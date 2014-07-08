#!/usr/bin/python
# James Tobat, 7/8/2014
# Pulls schema templates from 00-schema-examples
# file and returns an array of all the schemas in the file
import json
import sys
import collections

# Given a JSON schema, it will clear all values
# and return a blank schema to be filled out.
def clear_schema(schema):
  for key, value in schema.iteritems():
    if isinstance(value, list):
      schema[key] = [""]
    else:
      schema[key] = ""

  return schema

# Obtain schema templates from master schema file.
# Will also return the type of schema along with it.
def get_schemas():
  schema_list = []
  # Locations of important files/folders
  file_name = "00-schema-examples.json"
  data_dir = "../darpa_open_catalog/"
  schema_file = data_dir + file_name
  json_object = None

  # Loads the schemas from the master/examples file, preserves order
  try:
    schemas = json.load(open(schema_file), object_pairs_hook=collections.OrderedDict)
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % schema_file
    print " Details: %s" % str(e)
    sys.exit(1)

  for schema in schemas:
    schema_list.append(schema['Type'])
    blank_schema = clear_schema(schema['Schema'][0])
    schema_list.append(blank_schema)
  
  return schema_list
    
