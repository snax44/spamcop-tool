#!/usr/bin/python3
#coding:utf-8
###
#
# Author: snax44
# Date: 2021.05.13
# Desc:
#   - Test if IPs are blacklisted by Spamcop
#
###

import dns
import dns.resolver
import argparse
import ipaddress

VERBOSE = int(0)

def revert_ip(IP):
  A, B, C, D = IP.split('.')
  return ('{}.{}.{}.{}'.format(D, C, B, A))

def test_ip(IP_2_TEST):
  REVERTED_IP = revert_ip(IP_2_TEST)
  try:
    dns.resolver.resolve('{}.bl.spamcop.net'.format(REVERTED_IP), 'A')
  except:
    if VERBOSE >= 2:
      print("{} is not a spammer according Spamcop".format(IP_2_TEST))
    else:
      None
  else:
    if VERBOSE >= 1:
      print("{} is a spammer according Spamcop".format(IP_2_TEST))
    elif VERBOSE == 0:
      print(IP_2_TEST)

def main():
  global parser
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", type=str, help="Test list of IPs stored in a file (One by line)")
  parser.add_argument("-i", "--ip", type=str, help="Test one IP")
  parser.add_argument("-b", "--blocip", type=str, help="Test a bloc IP with CIDR notation")
  parser.add_argument("-v", "--verbose", action="count",default=0, help="Increase output verbosity")
  global args
  args = parser.parse_args()

  if args.verbose:
    global VERBOSE
    VERBOSE = int(args.verbose)

  if args.file:
    FILE = open(args.file, 'r')
    LINES = FILE.read().splitlines()
    FILE.close()

    for LINE in LINES:
      test_ip(LINE)

  elif args.ip:
    test_ip(args.ip)

  elif args.blocip:
    IP_LIST = ipaddress.ip_network(args.blocip)

    for IP in IP_LIST.hosts():
      test_ip(str(IP))

if __name__ == '__main__':
    main()
