#!/usr/bin/env python

import getopt
import os
import re
import sys

__author__ = "Erik Smartt"
__copyright__ = "Copyright 2010, Erik Smartt"
__license__ = "MIT"
__version__ = "0.2.3"
__usage__ = """Normal usage:
  cssreflow.py INPUT-FILE [OPTIONS] > OUTPUT-FILE

  Options:
    --alphaprops      Alphabetizes the CSS properties. [Default: off]
    --alphaselector   Alphabetizes the CSS selectors (potentially altering inheritence rules.) [Default: off]
    --clean           Shortcut for 2-space indent with alpha-props.
    --erik            Shortcut for flat with alphaprops, -alphaselectors, and line breaks between selector types.
    --flat            Puts declarations/rules on a single line.
    --help            Prints this Help message.
    --indent          Indent properties. [Default: on]
    --indentsize      Set the indent size. [Default: 2]
    --scan            Shortcut for silent, with warnings and errors displayed.
    --silent          Does not output the formatted text.
    --spaces          Use spaces to indent. [Default: on]
    --tabs            Use tabs to indent. [Default: off]
    --verbose         Output lots of information about the parsing process.
    --version         Print the version number of cssreflow being used.
"""

def get_config(options={}):
  # Setup default config (alter with command-line flags)
  config = {}

  config['before_type_change'] = ''

  config['before_selector'] = ''
  config['after_selector'] = ' '

  config['before_open_brace'] = ''
  config['after_open_brace'] = ''

  config['before_property'] = ''
  config['after_property'] = ''

  config['before_colon'] = ''
  config['after_colon'] = ' '

  config['before_value'] = ''
  config['after_value'] = ''

  config['before_semicolon'] = ''
  config['after_semicolon'] = ' '

  config['before_close_brace'] = '\n'
  config['after_close_brace'] = '\n'

  config['alphabetize_selectors'] = False
  config['alphabetize_properties'] = False

  config['indent'] = True
  config['indent_size'] = 2
  config['indent_with'] = ' '

  config['make_properties_lower_case'] = True
  config['make_values_lower_case'] = True

  config['verbose'] = False

  # Add/change settings based on values in 'options'
  for k in options:
    config[k] = options[k]

  return config


def parse_file(file_name, config):
  # Might be able to clean this up using Python 3.1's sorted dictionary someday...
  data = {'__keys__':[], '__errors__':[], '__warnings__':[]}

  if (not (os.path.exists(file_name))):
    print "\n--------------------------\nERROR: File not found.\n--------------------------\n"
    return data

  if (not (os.path.isfile(file_name))):
    print "\n--------------------------\nERROR: Not a valid file.\n--------------------------\n"
    return data

  fp = open(file_name, 'r')
  text = fp.read()
  fp.close()

  #print "Parsing: %s" % (file_name)

  re_statement = re.compile("""
    ^                               # From the beginning of a line
    \s*                             # Take any amount of whitespace
    ([\#\.\ a-zA-Z0-9\-\_\@\:]+)    # Match a variety of legal CSS class, id, tag, etc. characters
    \s*                             # Any whitespace
    {(.*?)}                         # Anything wrapped in {} braces
  """, re.M|re.S|re.VERBOSE)

  #re_property = re.compile("([-\w]+)\s*:\s*([\\\/\:\'\"\(\)\#\%\_\-\.\ a-zA-Z0-9]+)\s*;", re.M|re.S)
  # Rather than explicitly allowing chars (as above), we'll take anything that isn't a semi-colon
  re_property = re.compile("""
    ([-\w]+)           # At least one character
    \s*:\s*            # A colon surounded by any amount of whitespace
    ([^\;]+)           # Anything but a semicolon
    \s*;               # Any amount of whitespace, followed by a semi-colon
  """, re.M|re.S|re.VERBOSE)

  for mo in re_statement.finditer(text):
    if mo:
      selector = mo.group(1).strip()
      property_string = mo.group(2)
      property_set = []

      if config['verbose']: print "parse_file('%s'): Found selector: %s" % (file_name, selector)

      if data.has_key(selector):
        data['__warnings__'].append("Found duplicate selector '%s'" % (selector))
      else:
        data[selector] = {'__keys__':[]}
        data['__keys__'].append(selector)

      for po in re_property.finditer(property_string):
        if po:
          attr = po.group(1).strip()
          val = po.group(2).strip()

          if config['verbose']: print "parse_file('%s'): Found attribute: %s -> %s" % (file_name, attr, val)

          if data[selector].has_key(attr):
            data['__errors__'].append("Found duplicate attribute '%s' on selector '%s'" % (attr, selector))

          data[selector]['__keys__'].append(attr)
          data[selector][attr] = val

      if config['alphabetize_properties']:
        data[selector]['__keys__'].sort()

    if config['alphabetize_selectors']:
      data['__keys__'].sort()

  return data


def structure_to_string(data, config):
  """
  @param    data    is a dictionary of everything
  @param    keys    is a sorted list of style statements
  """
  output = []
  previous_type = '' # class, tag, or ID
  current_type = ''

  for statement in data['__keys__']:
    try:
      current_type = statement[0]
    except:
      current_type = ''

    if config['before_type_change']:
      if ((current_type != previous_type) and ((previous_type == '.') or (previous_type == '#'))):
        output.append(config['before_type_change'])

    previous_type = current_type

    output.append(config['before_selector'])
    output.append(statement)
    output.append(config['after_selector'])
    output.append(config['before_open_brace'])
    output.append('{')
    output.append(config['after_open_brace'])

    for attr in data[statement]['__keys__']:
      if config['indent']:
        output.append('\n');
        for i in range(0, config['indent_size']):
          output.append(config['indent_with'])

      output.append(config['before_property'])
      output.append(attr)
      output.append(config['after_property'])

      output.append(config['before_colon'])
      output.append(':')
      output.append(config['after_colon'])

      output.append(config['before_value'])
      output.append(data[statement][attr])
      output.append(config['after_value'])

      output.append(config['before_semicolon'])
      output.append(';')
      output.append(config['after_semicolon'])

    # Replace the last 'after_semicolon' with whatever should be 'before_close_brace'.
    output[-1] = config['before_close_brace']
    output.append('}')
    output.append(config['after_close_brace'])

  return ''.join(output)


def run(mode_list):
  try:
    opts, args = getopt.getopt(mode_list[2:], "", ["alphaprops", "alphaselectors", "clean", "erik", "flat", "help", "indent", "indentsize=", "errors", "scan", "silent", "spaces", "tabs", "warn", "verbose", "version"])
    flatopts = map(lambda t: t[0], opts)

  except getopt.GetoptError, err:
    print str(err)
    print __usage__
    sys.exit(2)

  if (len(mode_list) < 2):
    print __usage__
    sys.exit(2)

  # First handle commands that exit
  if "--help" == mode_list[1]:
    print __usage__
    sys.exit(2)

  if "--version" == mode_list[1]:
    print __version__
    sys.exit(2)

  try:
    infile = mode_list[1]
  except IndexError:
    print "\n--------------------------\nERROR: Missing input file.\n--------------------------\n"
    print __usage__
    sys.exit(2)

  config = get_config()
  
  if "--alphaprops" in flatopts:
    config['alphabetize_properties'] = True

  if "--alphaselectors" in flatopts:
    config['alphabetize_selectors'] = True

  if "--clean" in flatopts:
    config['after_semicolon'] = ''
    config['alphabetize_selectors'] = False
    config['alphabetize_properties'] = True
    config['indent_size'] = 2
    config['indent_with'] = ' '

  if "--erik" in flatopts:
    config['alphabetize_selectors'] = True
    config['alphabetize_properties'] = True
    config['indent'] = False
    config['before_close_brace'] = ''
    config['before_type_change'] = '\n'

  if "--flat" in flatopts:
    config['indent'] = False
    config['before_close_brace'] = ''

  if "--indent" in flatopts:
    config['indent'] = True

  for o, a in opts:
    if o in ["--indentsize"]:
      config['indent_size'] = int(a)

  if "--spaces" in flatopts:
    config['indent_with'] = ' '

  if "--tabs" in flatopts:
    config['indent_with'] = '\t'


  if "--scan" in flatopts:
    flatopts.append('--silent')
    flatopts.append('--warn')
    flatopts.append('--errors')

  if "--verbose" in flatopts:
    config['verbose'] = True


  data = parse_file(infile, config)

  # Handle flags for optional output
  if "--warn" in flatopts:
    if data['__warnings__']:
      for msg in data['__warnings']:
        print 'WARNING: %s' % (msg)

  if "--errors" in flatopts:
    if data['__errors__']:
      for msg in data['__errors__']:
        print 'ERROR: %s' % (msg)

  if "--silent" in flatopts:
    pass
  else:
    return structure_to_string(data, config)



# ---------------------------------
#          MAIN
# ---------------------------------
if __name__ == "__main__":
  print run(sys.argv)

  sys.exit(2)
