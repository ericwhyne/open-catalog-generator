#!/usr/bin/python
# James Tobat, 2014
import json
import re
import sys
import glob
import os

# Finds the location in the JSON document of the script (line/col).
# Also sends an exit code to the Makefile.
def found_script_error(file_name, value):
  line_num = 1
  error_file = open(file_name)
  name_nopath = os.path.basename(file_name)
  for line in error_file:
    column = line.find(value)
    if column < 0:
      line_num+=1
    else:
      print "\nERROR: Found embedded html in file %s, line %i column %i" % (name_nopath, line_num, column)
  error_file.close()
  return
  
# Identifies if the given value (string) has an html tags inside of it.
# Will pick out html tags that have single value <h> or <img /> as well
def is_html(value):
  # will ignore br html tags, can be commented out
  # value = value.replace('<br>',' ') 
  # value = value.replace('<br/>',' ')
  html_opentag = re.search('<[a-zA-Z][^>]*>', value, re.I)
  html_closetag = re.search('</[a-zA-Z][^>]*>', value, re.I)
  if html_opentag or html_closetag:
    return value
  else:
    return 0

# Iterates through a json object (all keys/values) and
# tests each value to see if it has a script inside of it.
def test_for_xss(json_data, identifier):
  found_error = 0
  for key, value in json_data.iteritems():
    html = 0
    if isinstance(value, basestring) and value != "":
      html = is_html(value)
    elif isinstance(value, list):
      for item in value:
        if(item != ""):
          html = is_html(item)

    if html:
      found_script_error(identifier, html)
      found_error = 1

  return found_error

data_dir = sys.argv[1]
path = data_dir + '/*.json'

# Iterates through all JSON files in the directory
# provided to the script.
found_errors = 0

for file_name in glob.glob(path):
  name_nopath = os.path.basename(file_name)
  json_file = open(file_name)
  try:
    json_content = json.load(json_file)
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % name_nopath
    print " Details: %s" % str(e)
    sys.exit(1)

  json_file.close()
  if isinstance(json_content, dict):
    found_errors += test_for_xss(json_content, file_name)
  else:
    for record in json_content:
      found_errors += test_for_xss(record, file_name)

if found_errors:
  sys.exit(1)

  
