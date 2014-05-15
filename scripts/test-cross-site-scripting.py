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
      print "\nERROR: Found embedded script in file %s, line %i column %i" % (name_nopath, line_num, column) 
      sys.exit(1)
  error_file.close()
  return
  
# Identifies if the given value (string) has an html script inside of it.
# Will pick out html script tags with/without attributes e.g. <script src="">.
def is_script(value):
  script_attributes = re.search('<script .*>.*</script>', value, re.I)
  script_no_attributes = re.search('<script>.*</script>', value, re.I)
  if script_attributes or script_no_attributes:
    return value
  else:
    return 0

# Iterates through a json object (all keys/values) and
# tests each value to see if it has a script inside of it.
def test_for_xss(json_data, identifier):
  for key, value in json_data.iteritems():
    script = 0
    if isinstance(value, basestring) and value != "":
      script = is_script(value)
    elif isinstance(value, list):
      for item in value:
        if(item != ""):
	  script = is_script(item) 

    if script:
      found_script_error(identifier, script)

  return 

data_dir = sys.argv[1]
path = data_dir + '/*.json'

# Iterates through all JSON files in the directory
# provided to the script.
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
    test_for_xss(json_content, file_name)
  else:
    for record in json_content:
      test_for_xss(record, file_name)
  
