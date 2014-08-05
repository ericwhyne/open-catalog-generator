#!/usr/bin/python
import json
import re
import sys
import time
import os
import shutil
from pprint import pprint
import collections

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
new_json_dir = sys.argv[3]
schema_file = sys.argv[4]
date = time.strftime("%Y-%m-%d", time.localtime())
office_store = []
file_type_store = {"program", "pubs", "software", "office"}

file_types = ["program","software"] #"program", "pubs", "software, office"
new_fields = {"Test Options":["Pass","Fail","Undetermined"]} #{"New Date": "", "Update Date": ""}, {"Display Pubs Columns":["Team","Title","Link"]}
insert_after = "Program Teams" #"" or field name, e.g. "Display Software Columns" ,DARPA Office Color, placement of field

print len(sys.argv)

#if len(sys.argv) > 4:
#  for i in range(5, len(sys.argv)):
#    print 'i in loop:', sys.argv[i]
   # files_to_fix.append(sys.argv[i])
   
#sys.exit(1)   

print """
Active content file: %s
Data directory: %s
New JSON directory: %s
""" % (active_content_file, data_dir, new_json_dir)

#definition of add_fields_to_json method called later in code
def add_fields_to_json(object_name, original_file, schema_dict, file_type, new_file):
  for definition in schema_dict:
    def_keys = definition.keys()
    print 'schema definition keys: %s \n\r' % (def_keys)
  new_docs = collections.OrderedDict()
  new_doc = []
  if insert_after != "":
    if insert_after not in def_keys:
      print "\nFAILED! The key '%s' does not exist in the %s schema. Please use a valid key to insert new fields in the designated place." % (insert_after, file_type)
      sys.exit(1)
  if file_type == "office" or file_type == "program":
    recreate_fields = collections.OrderedDict()  
    for dkey in def_keys:
      print 'orig file: %s \n\r' % (original_file)
      for obj_key in original_file:
        if obj_key == dkey:
          print 'key: %s value: %s \n\r' % (obj_key, original_file[obj_key])
          recreate_fields[obj_key] = original_file[obj_key]
          if obj_key == insert_after:
            for field in new_fields:
              recreate_fields[field] = new_fields[field]
    if insert_after == "":
      for field in new_fields:
        print 'fields - %s : %s\n\r' % (field, new_fields[field])
        recreate_fields[field] = new_fields[field]		
    new_doc = recreate_fields
  if file_type == "software" or file_type == "pubs":
    for doc in original_file:
      object_keys = doc.keys()
      recreate_fields = collections.OrderedDict()
      print "keys: %s \n\r fields: %s" % (object_keys, recreate_fields)	  
      for dkey in def_keys:
        for obj_key in object_keys:
          if obj_key == dkey:
            print '%s: %s is present in schema \n\r' % (dkey, doc[dkey])
            recreate_fields[obj_key] = doc[obj_key]			
            if obj_key == insert_after:
              for field in new_fields:
                recreate_fields[field] = new_fields[field]
      if insert_after == "":
        for field in new_fields:
          print 'fields - %s : %s\n\r' % (field, new_fields[field])
          recreate_fields[field] = new_fields[field]     
      new_doc.append(recreate_fields)
  try:
    new_docs = new_doc
    print 'new file: \n %s \n\r' % new_docs
    new_json_object = json.dumps(new_docs, indent=4, separators=(',',':'))
    new_json_file = new_json_dir + new_file
    print "Writing to %s \n" % new_json_file
    json_outfile = open(new_json_file, 'w')
    json_outfile.write(new_json_object)
  except Exception, e:
    print "\nFAILED! Could not create new %s json file for %s" % (file_type, object_name)
    print " Details: %s" % str(e)
    sys.exit(1)	  

#set active content and schema files	
try:
  active_content = json.load(open(active_content_file))
except Exception, e:
  print "\nFAILED! JSON error in file %s" % active_content_file
  print " Details: %s" % str(e)
  sys.exit(1)

try:
  schemas = json.load(open(schema_file), object_pairs_hook=collections.OrderedDict)
except Exception, e:
  print "\nFAILED! JSON error in file %s" % schema_file
  print " Details: %s" % str(e)
  sys.exit(1)

#Start looping through active content to find the files that need to be modified  
for content in active_content:
  object_name = content['Program Name'].upper()
  if content['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % object_name
    sys.exit(1)
  else:
    for file_type in file_types:
      print "object: %s \r" % (object_name)	
      print "content: %s \r" % (content)
      print "file_type: %s \n" % file_type
      for schema in schemas:
        #Get Software Schema fields
        try:
          if file_type not in file_type_store:
            print "\nFAILED! The file or schema type being used is invalid. Valid file types are: office, program, software, pubs \n\r '%s' may not be a valid file type and will need to be added to the schema json and script to fix the issue." % file_type 
            sys.exit(1)	  
          if schema["Type"] == "Software" and file_type == 'software' and content['Software File'] != "":
            orig_software_file = data_dir + content['Software File']
            software = json.load(open(orig_software_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(object_name, software, schema_dict, file_type, object_name + '-' + file_type + '.json')
          if schema["Type"] == "Publication" and file_type == 'pubs' and content['Pubs File'] != "":
            orig_pubs_file = data_dir + content['Pubs File']
            pubs = json.load(open(orig_pubs_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(object_name, pubs, schema_dict, file_type, object_name + '-' + file_type + '.json')
          if schema["Type"] == "Program"  and file_type == 'program' and content['Program File'] != "":
            orig_program_file = data_dir + content['Program File']
            program = json.load(open(orig_program_file))
            schema_dict = schema["Schema"]
            add_fields_to_json(object_name, program, schema_dict, file_type, object_name + '-' + file_type + '.json')
          if schema["Type"] == "Office"  and file_type == 'office' and content['DARPA Office'] != "":
            if content['DARPA Office'] not in office_store:
              object_name = content['DARPA Office']			
              orig_office_file = data_dir + '01-DARPA-' + object_name + '.json'
              office = json.load(open(orig_office_file))
              office_store.append(object_name)
              schema_dict = schema["Schema"]
              add_fields_to_json(object_name, office, schema_dict, file_type, '01-DARPA-' + object_name + '.json')		  
        except Exception, e:
          print "\nFAILED! Problem with adding new json fields to %s %s file\n" % (object_name, file_type)
          print " Details: %s" % str(e)
          sys.exit(1)  