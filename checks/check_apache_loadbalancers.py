#!/usr/bin/env python

import argparse
import collections
import logging
import nagiosplugin
import urllib2

from bs4 import BeautifulSoup, SoupStrainer

class ApacheLoadBalancer(nagiosplugin.Resource):
  def __init__(self, url="", balancer=None):
    self.url = url
    self.balancer = balancer

  def get_balancers(self):
    soup = BeautifulSoup(urllib2.urlopen(self.url))

    balancers = []

    # find the h1 that contains LoadBalancer Status
    for tag in soup.find_all("h1"):
      if "Proxy LoadBalancer Status" in tag.string:
        if self.balancer is None or self.balancer in tag.string:
          # get the balancer name
          name = tag.string[tag.string.index("balancer://") + len("balancer://"):]
          
          # find all td's in the 2nd table with the text == Ok
          alive_members = tag.find_next_sibling("table").find_next_sibling("table").find_all("td", text="Ok")
          balancers.append((name, len(alive_members)))

    # If no balancers are found, return -1
    return balancers

  def probe(self):
    logging.info('checking status from %s' % (self.url))
    balancers = self.get_balancers()
    if len(balancers) > 0:
      for balancer in balancers:
        yield nagiosplugin.Metric(balancer[0], balancer[1], min=0, context='members')
    else:
      yield nagiosplugin.Metric('balancers', int(-1), min=0, context='members')

  @staticmethod
  @nagiosplugin.guarded
  def main():
    argp = argparse.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warning', metavar='RANGE', default='',
                      help='return warning if Ok members is outside RANGE')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='',
                      help='return critical if Ok members is outside RANGE')
    argp.add_argument('-b', '--balancer', action='store', default=None,
                      help='which balancer to check')
    argp.add_argument('url', help='apache server status url')
    args = argp.parse_args()

    check = nagiosplugin.Check(
        ApacheLoadBalancer(args.url, args.balancer),
        nagiosplugin.ScalarContext(
          'members', args.warning, args.critical
        ))

    check.main()

if __name__ == '__main__':
    ApacheLoadBalancer.main()
