# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import print_function

import argparse
import subprocess
import sys
import re


def Redact(value, from_nth_char=5):
  """Redact value past the N-th character."""
  return value[:from_nth_char] + '*' * (len(value) - from_nth_char)


class Identity(object):
  """Represents a valid identity."""

  def __init__(self, identifier, name, team):
    self.identifier = identifier
    self.name = name.encode('unicode_escape').decode('ascii')
    self.team = team

  def redacted(self):
    return Identity(Redact(self.identifier), self.name, Redact(self.team))

  def format(self):
    return '%s: "%s (%s)"' % (self.identifier, self.name, self.team)


def ListIdentities():
  return subprocess.check_output([
      'xcrun',
      'security',
      'find-identity',
      '-v',
      '-p',
      'codesigning',
  ]).decode('utf8')


def FindValidIdentity(cert_type, team_name):
  """Find all identities matching the cert type and team name."""
  lines = list(l.strip() for l in ListIdentities().splitlines())
  # Look for something like "2) XYZ "iPhone Developer: Name (ABC)""
  regex = re.compile('[0-9]+\) ([A-F0-9]+) "([^"(]*) \(([^)"]*)\)"')

  result = []
  for line in lines:
    res = regex.match(line)
    if res is None:
      continue
    if cert_type is None:
      result.append(Identity(*res.groups()))
    elif not team_name:
      if cert_type in res.group(2):
        result.append(Identity(*res.groups()))
    elif VerifyIdentityTeamName(line, cert_type, team_name):
      result.append(Identity(*res.groups()))
  return result


def VerifyIdentityTeamName(content, cert_pattern, team_pattern):
  """Verify that the team name of certificate identity matches the pattern"""
  # Look for something like "Apple Development: Name (ABC)"
  regex = re.compile('''[^"]+"(%s:[^"]+)"''' % cert_pattern)
  res = regex.match(content)
  if res is None:
    return False

  full_identity = res.groups()
  result = subprocess.check_output([
    'xcrun',
    'security',
    'find-certificate',
    '-c',
    '%s' % full_identity,
  ]).decode('utf8')

  match = False
  for line in result.split('\n'):
    line = line.strip()
    if line.startswith('''"subj"<blob>=''') and line.find(team_pattern) > 0:
      match = True
      break
  return match

def Main(args):
  parser = argparse.ArgumentParser('codesign iOS bundles')
  parser.add_argument('--cert-pattern',
                      dest='cert',
                      help='Cert type pattern used to select the code signing identity.')
  parser.add_argument('--team-pattern',
                      dest='team',
                      help='Team name pattern used to select the code signing identity.')
  parsed = parser.parse_args(args)

  identities = FindValidIdentity(parsed.cert, parsed.team)
  if len(identities) == 1:
    print(identities[0].identifier, end='')
    return 0

  all_identities = FindValidIdentity(None, None)

  print('Automatic code signing identity selection was enabled but could not')
  print('find exactly one codesigning identity matching "%s".' % parsed.cert)
  print('')
  print('You can override the `ios_code_signing_identity_team_name` args to ')
  print('filter out the codesigning identity of the specified team name.')
  print('')
  print('Check that the keychain is accessible and that there is exactly one')
  print('valid codesigning identity matching the pattern. Here is the parsed')
  print('output of `xcrun security find-identity -v -p codesigning`:')
  print()
  for i, identity in enumerate(all_identities):
    print('  %d) %s' % (i + 1, identity.redacted().format()))
  print('    %d valid identities found' % (len(all_identities)))
  return 1


if __name__ == '__main__':
  sys.exit(Main(sys.argv[1:]))
