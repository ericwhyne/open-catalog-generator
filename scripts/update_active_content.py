#!/usr/bin/python
# James Tobat, 8/24/2015
# Updates the active content file (active_content.json)
#
import json
import sys
import collections
import argparse

# Builds command line menu, requires three string arguments, and provides a help menu when the -h option is used.
parser = argparse.ArgumentParser(description='Update the active content file.')
parser.add_argument('active_directory', type=str, help='The directory of the active content json file.')
parser.add_argument('new_field', type=str, help='Name of the field to add to each entry in the active content file.')
parser.add_argument('insert_after', type=str, help='Name of attribute to inert the new field after', nargs='?')
parser.add_argument('-d', action='store_true', help='Change the active_content_deployed.json file instead')

args = vars(parser.parse_args())
new_field = args['new_field']
insert_after = args['insert_after']
use_deployed = args['d']

# Locations of important files/folders
active_file = args['active_directory'] + 'active_content.json' # Name of active content file.
deployed_file = args['active_directory'] + 'active_content_deployed.json' # Location of deployed active content file

json_file = None
if use_deployed:
  json_file = deployed_file
else:
  json_file = active_file

try:
  json_data = json.load(open(json_file), object_pairs_hook=collections.OrderedDict)
except Exception, e:
  print "\nFAILED! JSON error in file %s" % json_file
  print " Details: %s" % str(e)
  sys.exit(1)

new_json = []
changed_file = False
changed_order = False
for entry in json_data:
  json_object = collections.OrderedDict()
  if not new_field in entry:
    if insert_after:
      for key in entry:
        json_object[key] = entry[key]
        if key == insert_after:
          json_object[new_field] = ""
      new_json.append(json_object)
      changed_order = True 
    else:
      entry[new_field] = ""

    changed_file = True

if changed_file:
  if changed_order:
    json_data = new_json
  try:
    with open(json_file, 'w') as output:
      json.dump(json_data, output, sort_keys = False, indent=4, separators=(',',':'), ensure_ascii=False)
  except Exception, e:
    print "\nFAILED! Could not update %s json file" % json_file
    print " Details: %s" % str(e)


