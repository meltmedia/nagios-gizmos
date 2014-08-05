#!/usr/bin/env python
import argparse
import boto
import boto.sqs
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

            name = '%s.%s' % (region, queue.name)
            yield nagiosplugin.Metric(name, queue.count(), context='count')

    def get_queues(self):
        for region in self.regions:
            conn = boto.sqs.connect_to_region(region)
            for q in conn.get_all_queues(prefix=self.prefix):
                q.set_message_class(boto.sqs.message.RawMessage)

                yield (region, q)


@nagiosplugin.guarded
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-w', '--warning', metavar='RANGE', default='',
        help='return warning if the message count is outside of RANGE')
    parser.add_argument(
        '-c', '--critical', metavar='RANGE', default='',
        help='return critical if the message count is '
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
        nagiosplugin.ScalarContext('count', args.warning, args.critical))

    check.main()

    return


if __name__ == '__main__':
    main()
