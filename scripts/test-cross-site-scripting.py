#!/usr/bin/python
# James Tobat, 2014
from HTMLParser import HTMLParser
import json
import sys
import glob
import os

class MyHTMLParser(HTMLParser):
    def __init__(self):
      HTMLParser.__init__(self)
      self.found_opentag = 0 
      self.found_closetag = 0
      self.found_openclosetag = 0
      self.found_tag = 0

    def handle_starttag(self, tag, attrs):
        self.found_opentag += 1

    def handle_endtag(self, tag):
        self.found_closetag += 1
    
    def handle_startendtag(self, tag, attrs):
        self.found_openclosetag += 1
    
    def identify_html(self):
        if self.found_opentag > 0 and self.found_closetag > 0:
          if self.found_opentag == self.found_closetag:
            self.found_tag = 1
        elif self.found_openclosetag > 0:
            self.found_tag = 1
        else:
            self.found_tag = 0
    

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
      print "\nERROR: Found embedded script/html in file %s, line %i column %i" % (name_nopath, line_num, column) 
      sys.exit(1)
  error_file.close()
  return
  
# Identifies if the given value (string) has a html tags inside of it
# Will pick any html tags even self containing html.
def is_html(value):
  parser = MyHTMLParser()
  parser.feed(value)
  parser.identify_html()
  html = parser.found_tag
  if html:
    return value
  else:
    return 0

# Iterates through a json object (all keys/values) and
# tests each value to see if it has a script inside of it.
def test_for_xss(json_data, identifier):
  parser = MyHTMLParser()
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
  
