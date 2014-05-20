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
new_json_dir = sys.argv[3]
schema_file = sys.argv[4]
date = time.strftime("%Y-%m-%d", time.localtime())

print """
Active content file: %s
Data directory: %s
New JSON directory: %s
""" % (active_content_file, data_dir, new_json_dir)

files_to_change = ["pubs", "software"] #"program", "pubs", "software"
fields_to_add = {"New Date": "", "Update Date": ""} #{"Display Pubs Columns":["Team","Title","Link"]}
insert_after = "" #"" or field name, e.g. "Display Software Columns"

def add_fields_to_json(program_name, original_file, schema_dict, file_type, new_file):
  for definition in schema_dict:
    def_keys = definition.keys()
    #print 'definition keys: %s \n\r' % (def_keys)
  new_docs = collections.OrderedDict()
  new_doc = []
  if file_type != "program":
    for doc in original_file:
      object_keys = doc.keys()
      new_fields = collections.OrderedDict()
      for dkey in def_keys:
        for obj_key in object_keys:
          if obj_key == dkey:
            #print '%s: %s is present in schema \n\r' % (dkey, doc[dkey])
            new_fields[obj_key] = doc[obj_key]
            if obj_key == insert_after:
              for field in fields_to_add:
                new_fields[field] = fields_to_add[field]
      if insert_after == "":
        for field in fields_to_add:
          #print 'fields - %s : %s\n\r' % (field, fields_to_add[field])
          new_fields[field] = fields_to_add[field]
      new_doc.append(new_fields)
  else:
    new_fields = collections.OrderedDict()  
    for dkey in def_keys:
      print 'orig file: %s \n\r' % (original_file)
      for obj_key in original_file:
        if obj_key == dkey:
          #print 'key: %s value: %s \n\r' % (obj_key, original_file[obj_key])
          new_fields[obj_key] = original_file[obj_key]
          if obj_key == insert_after:
            for field in fields_to_add:
              new_fields[field] = fields_to_add[field]
    if insert_after == "":
      for field in fields_to_add:
        #print 'fields - %s : %s\n\r' % (field, fields_to_add[field])
        new_fields[field] = fields_to_add[field]			  
    new_doc = new_fields
  try:
    new_docs = new_doc
    print 'new file: \n %s \n\r' % new_docs
    new_json_object = json.dumps(new_docs, indent=4, separators=(',',':'))
    new_json_file = new_json_dir + program_name + new_file
    print "Writing to %s \n" % new_json_file
    json_outfile = open(new_json_file, 'w')
    json_outfile.write(new_json_object)
  except Exception, e:
    print "\nFAILED! Could not create new %s json file for %s" % (file_type, program_name)
    print " Details: %s" % str(e)
    sys.exit(1)	  

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
    for file_type in files_to_change:
      print "filetype: %s \n" % file_type
      for schema in schemas:
        #Get Software Schema fields
        try:
          #print "schema type: %s , file type: %s, \n program: \n %s \n\r" %(schema["Type"], file_type, program) 
          if schema["Type"] == "Software" and file_type == 'software' and program['Software File'] != "":
            orig_software_file = data_dir + program['Software File']
            software = json.load(open(orig_software_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(program_name, software, schema_dict, file_type, '-' + file_type + '.json')
          if schema["Type"] == "Publication"  and file_type == 'pubs' and program['Pubs File'] != "":
            orig_pubs_file = data_dir + program['Pubs File']
            pubs = json.load(open(orig_pubs_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(program_name, pubs, schema_dict, file_type, '-' + file_type + '.json')
          if schema["Type"] == "Program"  and file_type == 'program' and program['Program File'] != "":
            orig_program_file = data_dir + program['Program File']
            program = json.load(open(orig_program_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(program_name, program, schema_dict, file_type, '-' + file_type + '.json')
        except Exception, e:
          print "\nFAILED! Problem with adding new json fields to %s %s file\n" % (program_name, file_type)
          print " Details: %s" % str(e)
          sys.exit(1)  