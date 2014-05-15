#!/usr/bin/python
import json
import re
import sys
import time
import os
import shutil
import darpa_open_catalog as doc
import sunburst_graphics as graph
from pprint import pprint
import collections

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
schema_file = sys.argv[3]
date = time.strftime("%Y-%m-%d", time.localtime())

print """
Active content file: %s
Data directory: %s
""" % (active_content_file, data_dir)


fields_to_add = {"New Date":"", "Update Date":""}

#To run script: ./scripts/add_dates_fields.py active_content.json /home/.../open-catalog-generator/darpa_open_catalog/
def add_fields_to_json(program_name, original_file, schema_dict, new_file):
  for definition in schema_dict:
    def_keys = definition.keys()
  new_docs = collections.OrderedDict()
  new_doc = []
  for doc in original_file:
    object_keys = doc.keys()
    new_fields = collections.OrderedDict()
    for dkey in def_keys:
  	for obj_key in object_keys:
	    if obj_key == dkey:
  		#print '%s: %s is present in schema \n\r' % (skey, doc[skey])
		  new_fields[obj_key] = doc[obj_key]
    for field in fields_to_add:
      #print 'fields - %s : %s\n\r' % (field, fields_to_add[field])
      new_fields[field] = fields_to_add[field]
    new_doc.append(new_fields)
  new_docs = new_doc
  #print 'new file: \n %s \n\r' % new_docs
  new_json_object = json.dumps(new_docs, indent=4)
  new_json_file = data_dir + program_name + new_file
  print "Writing to %s \n" % new_json_file
  json_outfile = open(new_json_file, 'w')
  json_outfile.write(new_json_object)	

try:
  active_content = json.load(open(active_content_file))
except Exception, e:
  print "\nFAILED! JSON error in file 1 %s" % active_content_file
  print " Details: %s" % str(e)
  sys.exit(1)

try:
  schemas = json.load(open(schema_file), object_pairs_hook=collections.OrderedDict)
except Exception, e:
  print "\nFAILED! JSON error in file 1 %s" % schema_file
  print " Details: %s" % str(e)
  sys.exit(1)
  
for program in active_content:
  program_name = program['Program Name'].upper()
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
    sys.exit(1)
  else:
    for schema in schemas:
      #Get Software Schema fields
      if schema["Type"] == "Software" and program['Software File'] != "":
        try:
          orig_software_file = data_dir + program['Software File']
          software = json.load(open(orig_software_file))
          schema_dict = schema["Schema"]
          add_fields_to_json(program_name, software, schema_dict, '-software-withdates.json')
        except Exception, e:
          print "\nFAILED! Problem with adding new json fields to %s software file\n" % program_name
          print " Details: %s" % str(e)
          sys.exit(1)
      if schema["Type"] == "Publication" and program['Pubs File'] != "":
        try:
          orig_pubs_file = data_dir + program['Pubs File']
          pubs = json.load(open(orig_pubs_file))
          schema_dict = schema["Schema"]
          add_fields_to_json(program_name, pubs, schema_dict, '-pubs-withdates.json')
        except Exception, e:
          print "\nFAILED! Problem with adding new json fields to %s pubs file\n" % program_name
          print " Details: %s" % str(e)
          sys.exit(1)	  