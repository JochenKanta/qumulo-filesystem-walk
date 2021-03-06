#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import argparse
from qwalk_worker import QWalkWorker


def main():
    parser = argparse.ArgumentParser(description='Walk Qumulo filesystem and do that thing.')
    parser.add_argument('-s', help='Qumulo hostname', required=True)
    parser.add_argument('-u', help='Qumulo API user', 
                              default=os.getenv('QUSER') or 'admin')
    parser.add_argument('-p', help='Qumulo API password',
                              default=os.getenv('QPASS') or 'admin')
    parser.add_argument('-d', help='Starting directory', required=True)
    parser.add_argument('-g', help='Run with filesystem changes', action='store_true')
    parser.add_argument('-l', help='Log file',
                              default='output-walk-log.txt')
    parser.add_argument('-c', help='Class to run. Options include: ' + \
                             'ChangeExtension, SummarizeOwners, DataReductionTest, ' + \
                             'ModeBitsChecker'
                            , required=True)

    try:
        # Will fail with missing args, but unknown args will all fall through.
        args, other_args = parser.parse_known_args()
    except:
        print("-"*80)
        parser.print_help()
        print("-"*80)
        sys.exit(0)

    QWalkWorker.run_all(args, other_args)

if __name__ == "__main__":
    main()