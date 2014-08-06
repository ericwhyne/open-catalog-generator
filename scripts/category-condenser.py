#!/usr/bin/python
# James Tobat, 8/6/2014
# Replaces a value in the supplied JSON attribute
# with a new value, all of these arguments are supplied
# by the user
import json
import sys
import glob
import os
import argparse
import get_schemas as gs
import collections

# Builds command line menu, requires three string arguments, and provides a help menu when the -h option is used.
parser = argparse.ArgumentParser(description='Replace a given value in a JSON attribute with the user supplied value.')
parser.add_argument('JSON_Attribute', type=str, help='Attribute that contains value to be changed.')
parser.add_argument('Old_Value', type=str, help='The old value that will be replaced by the new value.')
parser.add_argument('New_Value', type=str, help='Replacement value.')

args = vars(parser.parse_args())
key_value = args['JSON_Attribute'] # Attribute that has value for replacement
old_value = args['Old_Value'] # Value to be replaced
new_value = args['New_Value'] # Replacement value

# Returns a JSON object from a file, with its order preserved.
def open_JSON(json_file):
  try:
    json_data = json.load(open(json_file), object_pairs_hook=collections.OrderedDict)
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % json_file
    print " Details: %s" % str(e)
    sys.exit(1)	

  return json_data

# Replaces a value, matching the old value, with a new value
def replace_listvalue(list_name, old_value, new_value):
  i = 0
  changes = 0
  for item in list_name:
    if item == old_value:
      list_name[i] = new_value
      changes += 1
    i += 1
  return changes

# Changes a Categories value from one thing to another
# inside of a single JSON file
def update_JSON(json_file, old_value, new_value):
  # Tries to load JSON data into program
  json_data = open_JSON(json_file)
  file_name = os.path.basename(json_file)
  changes = 0

  # Checks to see if the data contains only 1 JSON record
  if isinstance(json_data, dict):
    # Finds the matching value in Categories and replaces it
    for key, value in json_data.iteritems():
      if key == key_value:
        if isinstance(value, list):
          changes += replace_listvalue(value, old_value, new_value)
        else:
          if value == old_value:
            json_data[key] = new_value
            changes += 1
  else:
    # Goes through all JSON records in JSON file
    for record in json_data:
      # Finds the matching value in Categories and replaces it
      for key, value in record.iteritems():
        if key == key_value: 
          if isinstance(value, list):
            changes += replace_listvalue(value, old_value, new_value)
          else:
            if value == old_value:
              record[key] = new_value
              changes += 1
  
  # Only writes updated JSON file if something changed
  if changes > 0:
    try:
      with open(json_file, 'w') as output:
        json.dump(json_data, output, sort_keys = False, indent = 4, ensure_ascii=False)
    except Exception, e:
      print "\nFAILED! Could not update %s json file for %s" % (file_name, program_name)
      print " Details: %s" % str(e)
    
    print "Changed %i entries in %s" % (changes, file_name)

  return changes

schemas = gs.get_schemas() # List of schemas from template file

# Determines the type of schemas given from the template file
for i in range(len(schemas)):
  if i % 2 == 0:
    if schemas[i] == "Publication":
      pub_schema = schemas[i+1]
    elif schemas[i] == "Software":
      software_schema = schemas[i+1]
    else:
      program_schema = schemas[i+1]

found_key = False # Boolean which determines if the user's key was
                  # found in any of the JSON schemas

# Paths of all JSON file types in the open catalog
path_pub = '../darpa_open_catalog/*-pubs.json'
path_software = '../darpa_open_catalog/*-software.json'
path_program = '../darpa_open_catalog/*-program.json'

search_files = [] # List of files to search in for the given user value

# Determines what types of JSON files the attribute is located
# in and will only search those files.
if key_value in pub_schema:
  found_key = True
  search_files.extend(glob.glob(path_pub))

if key_value in software_schema:
  found_key = True
  search_files.extend(glob.glob(path_software))

if key_value in program_schema:
  found_key = True
  search_files.extend(glob.glob(path_program))

# Indicates the key was not found in any of the schemas, meaning that the attribute
# was probably misspelled
if not found_key:
  print "Error: %s was not found in any of the JSON files.\nPlease make sure \
the attribute is spelled correctly." % key_value

changed = 0
# Updates each json file that requires a value to be replaced
# and then records the number of changes made.
for file_name in search_files:
  changed += update_JSON(file_name, old_value, new_value)

# Indicates that no JSON file was changes meaning that the value to be replaced was
# not found.
if not changed:
  print "No changes were made to any JSON files."




