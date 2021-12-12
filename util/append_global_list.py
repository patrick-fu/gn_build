#!/usr/bin/env python
# Copyright 2021 Patrick Fu. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os, sys, time, argparse

def Main():
  parser = argparse.ArgumentParser(description='A script to collect some values into a global file for GN.')
  parser.add_argument('--file', type=str, required=True, help='Path to the global list file')
  parser.add_argument('--expired-seconds', type=str, default='10', help='How many seconds can it take to execute "gn gen" command, usually set it to 10 sec')
  parser.add_argument('values', nargs='+', help='Values to be append to the file.')
  args = parser.parse_args()

  # Remove the previous build's file if needed
  stamp_file = '%s.stamp' % args.file
  current_timestamp = int(time.time())
  if os.path.exists(args.file):
    if os.path.exists(stamp_file):
      with open(stamp_file, 'r') as f:
        previous_timestamp = int(f.read())

      # If it is more than ${--expired-seconds} seconds since the last visit to the stamp file
      # it means that the build is not the same time, delete the file
      if current_timestamp - previous_timestamp > int(args.expired_seconds):
        if os.path.exists(args.file):
          os.remove(args.file)
  with open(stamp_file, 'w') as f:
    f.write(str(current_timestamp))

  # Now appends the values to the global file
  with open(args.file, 'a') as fw:
    for value in args.values:
      fw.write('%s\n' % value)

  return 0

if __name__ == '__main__':
  sys.exit(Main())
