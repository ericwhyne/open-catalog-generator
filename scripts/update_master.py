#!/usr/bin/python
# James Tobat, 7/7/2014
# Updates the master schema file (00-schema-examples.json)
# which means that it will retain all the old catagories
# and their values but will add new blank categories
import json
import sys
import collections
import argparse

# Builds command line menu, requires three string arguments, and provides a help menu when the -h option is used.
parser = argparse.ArgumentParser(description='Update the JSON schema template file with JSON schemas from a given DARPA Program Name.')
parser.add_argument('Schema_File', type=str, help='The name of the schema/template file.')
parser.add_argument('JSON_Files', type=str, help='Directory that contains the JSON files from which the template will be updated.')
parser.add_argument('DARPA_Program', type=str, help='Name of DARPA Program from which to pull schema updates from.')

args = vars(parser.parse_args())
# Locations of important files/folders
schema_file = args['Schema_File'] # Name of schema file.
json_files = args['JSON_Files'] # Location of JSON files with updates
program_name = args['DARPA_Program'] # DARPA Program Name
json_object = None

schema_file = json_files + schema_file

# Locations of files to copy/update from
updated_pub = json_files + program_name +'-pubs.json'
updated_software = json_files + program_name + '-software.json'
updated_program = json_files + program_name + '-program.json'

# Given a copy of the old schema, and the file location of
# a new schema to update from, it will match the old one
# with the new. The mode variable is for output purposes
# in order to show what schema has been changed.
def update_schema(old_schema, new_schema_file, mode):
  # Loads the updated/new schema into an OrderedDict, this is done
  # to preserve the order of the schema.
  try:
    json_data = json.load(open(new_schema_file), object_pairs_hook=collections.OrderedDict)
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % new_schema_file
    print " Details: %s" % str(e)
    sys.exit(1)

  # Checks to see if the json loaded is a dictionary (single entry)
  # or an array/list, if it is array, it will grab the first value
  if isinstance(json_data, dict):
    json_template = json_data
  else:
    json_template = json_data[0]

  changes = 0
  # Iterates through the JSON dictionary
  # and checks each key in the updated schema.
  # If it exists already, no change is made in the values
  # but if it doesn't exist, a blank value is placed
  # there or a list with a blank starting value. 
  for key, value in json_template.iteritems():
    if key not in old_schema:
      changes += 1
      if isinstance(value, list):
        json_template[key] = [""]
      else:
        json_template[key] = ""
    else:
      json_template[key] = old_schema[key]

  # Outputs a statement indicating if a template change
  # occurred
  if changes > 0:
    print "%i changes made to %s template" % (changes, mode)
    return json_template
  else:
    return 0

# Loads the schemas from the master/examples file, preserves order
try:
  schemas = json.load(open(schema_file), object_pairs_hook=collections.OrderedDict)
except Exception, e:
  print "\nFAILED! JSON error in file %s" % schema_file
  print " Details: %s" % str(e)
  sys.exit(1)

# Goes through each schema type in the master file and checks for updates
schemas_changed = 0
for schema in schemas:
  if schema['Type'] == 'Software':
    updated_schema = update_schema(schema['Schema'][0], updated_software, schema['Type'])
  elif schema['Type'] == 'Program':
    updated_schema = update_schema(schema['Schema'][0], updated_program, schema['Type'])
  else:
    updated_schema = update_schema(schema['Schema'][0], updated_pub, schema['Type'])

  if updated_schema:
    schemas_changed += 1
    schema['Schema'][0] = updated_schema
  
# Overwrites the existing schema inside of the master file if
# and only if changes were made
if schemas_changed > 0:
  try:
    with open(schema_file, 'w') as output:
      json.dump(schemas, output, sort_keys = False, indent=4, separators=(',',':'), ensure_ascii=False)
  except Exception, e:
    print "\nFAILED! Could not update %s json file for %s" % (schema_file, program_name)
    print " Details: %s" % str(e)
    
  

