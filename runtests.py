#!/usr/bin/env python

import hashlib
import os
import sys

__author__ = "Erik Smartt"
__copyright__ = "Copyright 2010, Erik Smartt"
__license__ = "MIT"

import cssreflow


def next_test_file(dirname):
  for root, dirs, files in os.walk(dirname):
    for filename in files:
      if filename.endswith('-in.css'):
        yield (dirname, filename)


def validate(inpath, mode, content):
  outpath = inpath.replace('-in', '-%s' % mode)

  fp = open(outpath, 'r')
  expected_output = fp.read()
  fp.close()

  # Hopefully this doesn't come back to bite me, but I'm using a hash of the
  # output to compare it with the known TEST PASS state.  The odds of a false
  # positive are pretty slim...
  if (hashlib.sha224(content).hexdigest() == hashlib.sha224(expected_output).hexdigest()):
    print "PASS [%s --%s]" % (inpath, mode)
  else:
    print "FAIL [%s --%s]" % (inpath, mode)

    # Write the expected output file for local diffing
    fout = open('%s_expected' % outpath, 'w')
    fout.write(content)
    fout.close()



# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
  print "Testing..."

  for directory, infile in next_test_file("testfiles"):
    inpath = "%s/%s" % (directory, infile)
    print "----\ntesting %s" % (inpath)

    for testmode in ['clean', 'flat', 'erik']:
      validate(inpath, testmode, cssreflow.run([None, inpath, '--%s' % (testmode)]))

  print "Done."

  sys.exit(2)

