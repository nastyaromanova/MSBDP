#!/usr/bin/env python

import sys
from operator import itemgetter 

transaction_map = {}

for line in sys.stdin:
    line = line.strip()
    try:
        country_city, count = line.split('\t')
        count = int(count)
        transaction_map[country_city] = transaction_map.get(reddit, 0) + count
    except ValueError:
        pass

sorted_transaction_map = sorted(transaction_map.items(), key=itemgetter(0))

for country_city, transactions in sorted_transaction_map:
    print(f'{country_city}\t{transactions}')