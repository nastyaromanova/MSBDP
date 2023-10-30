#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    columns = line.split(',') # split line into parts

    try:
        city = columns[11]
        country = columns[13]
        print(f'{country}:{city}\t{1}')
    except ValueError:
        pass