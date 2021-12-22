#!/usr/bin/env python
# Copyright 2021 Patrick Fu. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys, argparse

def Main():
  parser = argparse.ArgumentParser(description='A script to collect some values into a global file for GN.')
  parser.add_argument('--file', type=str, required=True, help='Path to the global list file')
  parser.add_argument('values', nargs='+', help='Values to be append to the file.')
  args = parser.parse_args()

  with open(args.file, 'a') as fw:
    for value in args.values:
      fw.write('%s\n' % value)

  return 0

if __name__ == '__main__':
  sys.exit(Main())
