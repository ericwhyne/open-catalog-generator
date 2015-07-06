#!/usr/bin/python
import json
import sys
jfile = open(sys.argv[1])
jstring = jfile.read()
try:
  json.loads(jstring)
except ValueError, e:
  print e
