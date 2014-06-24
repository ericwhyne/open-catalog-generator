#!/usr/bin/python
# James Tobat, 6/24/2014
# Replaces values in the Categories field
# in JSON files
import json
import sys
import glob
import os

program_name = "category-condenser"
key_value = "Categories"
old_value = sys.argv[1] # Value to be replaced
new_value = sys.argv[2] # Replacement value

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
  try:
    json_data = json.load(open(json_file))
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % json_file
    print " Details: %s" % str(e)
    sys.exit(1)	
  
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

  return

# Iterates through all pub/software JSON files in data directory
path_pub = '../darpa_open_catalog/*-pubs.json'
path_software = '../darpa_open_catalog/*-software.json'

for file_name in glob.glob(path_software):
  update_JSON(file_name, old_value, new_value)

for file_name in glob.glob(path_pub):
  update_JSON(file_name, old_value, new_value)


