#!/usr/bin/python
import json
import re
import sys
import time
import urllib2
import base64
import socket
from pprint import pprint

# This file is replaced by a tool called linkchecker. sudo apt-get install linkchecker
# to instantiate from open catalog generator make file:
# testurls:
#	$(OC_TEST_DIR)test_urls.py $(OC_ACTIVE_CONTENT_FILE) $(OC_DATA_DIR)

# timeout to wait in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

retval = 0
badurls = []
# In order to not hang on authentication fields we give it a bad username and password
headers = {'Authorization': 'Basic ' + base64.encodestring('faketestusername:faketestpassword')}

def is_url(text):
  if re.search("^http",text):
    return 1
  if re.search("^ftp",text):
    return 1  
  return 0

def find_and_test_urls(json_data, identifier):
  for key, value in json_data.iteritems():
    if isinstance(value, basestring) and value != "":
      if is_url(value):
        print "Testing url: " + value
        try:
          req = urllib2.Request(value, "", headers)
          resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
          problem = ""
          if hasattr(e, 'reason'):
            problem = " reason: " + str(e.reason)
          if hasattr(e, 'code'):
            problem = " code: " + str(e.code)
          notice = "Bad url in " + identifier + " had " + problem + " url: " + value
          print "  Status: " + notice
          badurls.append(notice)
          retval = 1
        except socket.error:
          notice = "Bad url in " + identifier + " had socket error (maybe timeout) url: " + value
          print "  Status: " + notice
          badurls.append(notice)
          retval = 1
        except:
          notice = "Bad url in " + identifier + " had unknown error url: " + value
          print "  Status: " + notice
          badurls.append(notice)
          retval = 1
        else:
          # code 200
          print "  Status: good"
  return 

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
date = time.strftime("%Y-%m-%d", time.localtime())

print "Attempting to load %s" %  active_content_file
active_content = json.load(open(active_content_file))

for program in active_content:
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file." % program_name
    sys.exit(1)
  else:
    something = 1
    print "Attempting to load %s" %  program['Program File']
    json_data = json.load(open(data_dir + program['Program File']))
    find_and_test_urls(json_data, "file: " + program['Program File'])

  if program['Software File'] != "":
    print "Attempting to load %s" %  program['Software File']
    json_data = json.load(open(data_dir + program['Software File']))
    for record in json_data:
      identifier = "file: " + program['Software File'] + " Record: \"" + record['Software'] + "\""
      if isinstance(record, dict):
        find_and_test_urls(record, identifier)
      else:
        print "Warning: could not load a record in " + identifier
        retval = 1   

  if program['Pubs File'] != "":
    print "Attempting to load %s" %  program['Pubs File']
    json_data = json.load(open(data_dir + program['Pubs File']))
    for record in json_data:
      identifier = "file: " + program['Pubs File'] + " Record: \"" + record['Title']  + "\""
      if isinstance(record, dict):
        find_and_test_urls(record, identifier)
      else:
        print "Warning: could not load a record in " + identifier
        retval = 1 

print "\n\nSummary of test ran " + date 
for badurl in badurls:
  print badurl
        
sys.exit(retval)



