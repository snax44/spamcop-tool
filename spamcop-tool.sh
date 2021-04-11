#!/bin/bash
###
#
# Author: Maël
# Date: 2021.04.11
# Desc:
#   - Test if IPs are blacklisted by Spamcop
#
###
set -e

function main(){
  if [ "$1" == "-f" ] || [ "$1" == "--file" ]; then

    while read -r line; do
      test_ip $line
    done < $2

  elif [ "$1" == "-b" ] || [ "$1" == "--blocip" ]; then

    if [ ! $(which nmap) ]; then
      echo ""
      echo "  This option [-b] required nmap. Please installed it:"
      echo "    apt install nmap"
      echo ""
      exit 1
    fi

    for e in $(nmap -sL -n $2 | awk '/Nmap scan report/{print $NF}'); do
      test_ip $e
    done

  elif [ "$1" == "-i" ] || [ "$1" == "--ip" ]; then

    test_ip $1

  elif [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
    exit 0
  else
    usage
    exit 1
  fi
}

function ip_revert(){
  IP_IN="$1"
  function cutter {
    echo $IP_IN | cut -d "." -f $1
  }
  IP_REVERTED="$(cutter 4).$(cutter 3).$(cutter 2).$(cutter 1)"
  echo "$IP_REVERTED"
}

function test_ip(){
  IP=$1
  if host $(ip_revert $IP).bl.spamcop.net > /dev/null; then
    echo "$1 is a spammer according Spamcop"
  fi
}

function usage(){
  cat <<EOM
Test if IPs are blacklisted by Spamcop

  Usage:
        $0 -i <ip_address>
        $0 -f <your_file>
        $0 -b <ip/cidr>

    -i  --ip        Test one IP
    -f  --file      Test list of IPs stored in a file (One by line)
    -b  --blocip    Test a bloc IP with CIDR notation
    -h  --help      Print this help

EOM
}
main $1 $2
