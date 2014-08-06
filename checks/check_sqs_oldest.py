#!/usr/bin/env python
import argparse
import boto
import boto.sqs
import datetime
import logging
import nagiosplugin


DEFAULT_REGIONS = ['us-east-1', 'us-west-1']


class CheckSQSOldest(nagiosplugin.Resource):
    def __init__(self, regions, prefix):
        self.regions = regions
        self.prefix = prefix

        if not self.regions:
            self.regions = DEFAULT_REGIONS

    def probe(self):
        for (region, queue) in self.get_queues():
            logging.debug('checking status for queue %s' % queue.name)
            oldest = self.get_oldest(queue)

            name = '%s.%s' % (region, queue.name)
            if not oldest:
                yield nagiosplugin.Metric(name, 0, context='oldest')
                continue

            now = datetime.datetime.now()
            then = datetime.datetime.fromtimestamp(oldest / 1000)

            delta = now - then

            minutes = delta.total_seconds() / 60

            yield nagiosplugin.Metric(name, minutes, context='oldest')

    def get_queues(self):
        for region in self.regions:
            conn = boto.sqs.connect_to_region(region)
            for q in conn.get_all_queues(prefix=self.prefix):
                q.set_message_class(boto.sqs.message.RawMessage)
                yield (region, q)

    def get_oldest(self, queue):
        messages = queue.get_messages(
            num_messages=10, visibility_timeout=0, attributes='SentTimestamp',
            wait_time_seconds=1)

        oldest = None
        for message in messages:
            sent = int(message.attributes['SentTimestamp'])
            if oldest is None or sent < oldest:
                oldest = sent

        return oldest


@nagiosplugin.guarded
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-w', '--warning', metavar='RANGE', default='',
        help='return warning if oldest message in minutes is outside of RANGE')
    parser.add_argument(
        '-c', '--critical', metavar='RANGE', default='',
        help='return critical if oldest message in minutes is '
        'outside of RANGE')
    parser.add_argument(
        '-r', '--region', action='append', default=None,
        help='set a region to check, can be repeated')
    parser.add_argument(
        '-p', '--prefix', default=None,
        help='Optionally, only return queues that start with this value.')

    args = parser.parse_args()

    check = nagiosplugin.Check(
        CheckSQSOldest(args.region, args.prefix),
        nagiosplugin.ScalarContext('oldest', args.warning, args.critical))

    check.main()

    return


if __name__ == '__main__':
    main()
