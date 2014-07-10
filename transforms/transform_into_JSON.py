#!/usr/bin/python
import sys
import json
import io
import os.path
import word_to_JSON as word
import csv_to_JSON as csv
from collections import OrderedDict
import argparse

file_types = [".csv",".docx"]
doc_path = "./documents/"
json_path = "./new_json/"
sys.path.insert(0, '../scripts')
import get_schemas as gs

def path_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)
    print "%s folder has been created." % path
    return False
  else:
    return True

path_exists(json_path)
if not path_exists(doc_path):
  print "Error: document folder is missing, please re-run script.\
\nPlease place documents to be transformed in documents folder."
  sys.exit(1)

def is_valid_file(parser, arg):
  fileExtension = os.path.splitext(arg)[1]
  if fileExtension not in file_types:
    parser.error("%s has an invalid file type.\nPlease use one of the following\
%s." % (arg, file_types))
  if not os.path.isfile(doc_path + arg):
    parser.error("%s does not exist." % arg)
  return arg

parser = argparse.ArgumentParser(description='Transform document into JSON.')
parser.add_argument('-t', action='store_true', help='Use schema template for transform')
parser.add_argument('mode', type=str, help='Mode for transformation', choices=['program','pubs','software'])
parser.add_argument('file_name', type=lambda x: is_valid_file(parser, x), help='List of files to be transformed, need at least 1', nargs='+')

args = vars(parser.parse_args())
mode = args['mode']
template = args['t']
schemas = gs.get_schemas()

# Matches the schema with the appropriate type after
# being 
for i in range(len(schemas)):
  print i
  if i % 2 == 0:
    if schemas[i] == "Publication":
      pub_schema = schemas[i+1]
    elif schemas[i] == "Software":
      software_schema = schemas[i+1]
    else:
      program_schema = schemas[i+1]

# Represents the schema that will be used in parsing
schema = 0

if mode == "pubs":
  schema = pub_schema
elif mode == "software":
  schema = software_schema
else:
  schema = program_schema

# Outputs a schema'd JSON file for the file given
def output_JSON(file_name):
  if file_name.endswith(".docx"):
    if args['t'] == True:
      print "Error: Template mode can only be used with csv's"
    else:
      JSON_data = word.parse_text(file_name,mode,schema)

  if file_name.endswith(".csv"):
    JSON_data = csv.parse_csv(file_name,mode,schema,template)

  outfile_name = JSON_data[0]
  outfile_path = json_path + outfile_name
    
  try:
    outfile = open(outfile_path, 'w')
    del JSON_data[0]
    json.dump(JSON_data, outfile, sort_keys = False, indent = 4, ensure_ascii=False)
  except Exception, e:
    print "Error: %s could not be created." % outfile_path
    print "Details: %s" % str(e)

  #print "%s has successfully been created." % outfile_name
  return

for doc in args['file_name']:
  doc_location = doc_path + doc
  output_JSON(doc_path + doc)

