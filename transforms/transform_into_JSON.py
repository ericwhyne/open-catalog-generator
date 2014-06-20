#!/usr/bin/python
import sys
import json
import io
import glob
import re
import word_to_JSON as word
import csv_to_JSON as csv
from collections import OrderedDict

# A parsing mode (pub, project, program) must be supplied as well
# as a document type (csv or docx for now)
if len(sys.argv) < 2:
  print "Error: Not enough arguments given, please supply a document type (ex. docx) and a mode (pub, project, program)"
  sys.exit()
else:
  mode = sys.argv[2]
  doc_type = sys.argv[1]

# Checks for files with the given document type in
# upper and lower case.
file_path1 = '*.' + doc_type.lower()
file_path2 = '*.' + doc_type.upper()

# Represents the schema that will be used in parsing
schema = 0
# Represents the schema for publications, it is an
# OrderedDict to ensure that the order that the entries
# are created are in the same order in output. Done to match
# the structure of existing JSON files
pub_schema = OrderedDict()
pub_schema['DARPA Program'] = ''
pub_schema['Program Teams'] = ['']
pub_schema['Title'] = ''
pub_schema['Authors'] = ['']
pub_schema['Link'] = ''
pub_schema['Categories'] = ['']
pub_schema['Subcategories'] = ['']
pub_schema['ACM 1998 classification code'] = ['']
pub_schema['New Date'] = ''
pub_schema['Update Date'] = ''

# Represents the schema for projects(software), it is an
# OrderedDict to ensure that the order that the entries
# are created are in the same order in output. Done to match
# the structure of existing JSON files
project_schema = OrderedDict()
project_schema['DARPA Program'] = ''
project_schema['Program Teams'] = ['']
project_schema['Contributors'] = ['']
project_schema['Sub-contractors'] = ['']
project_schema['Software'] = ''
project_schema['Internal Link'] = ''
project_schema['External Link'] = ''
project_schema['Public Code Repo'] = ''
project_schema['Instructional Material'] = ''
project_schema['Description'] = ''
project_schema['License'] = ['']
project_schema['Languages'] = ['']
project_schema['Platform Requirements'] = ['']
project_schema['Dependent modules'] = ['']
project_schema['Dependent module URLs'] = ['']
project_schema['Component modules'] = ['']
project_schema['Component module URLs'] = ['']
project_schema['Industry'] = ['']
project_schema['Functionality'] = ['']
project_schema['Categories'] = ['']
project_schema['New Date'] = ''
project_schema['Update Date'] = ''

# Checks to see if the mode given is valid.
# Can only parse in two modes for now.
if mode == 'pub':
  schema = pub_schema
elif mode == 'project':
  schema = project_schema
else:
  print "Error: Incorrect mode given, please use pub, project, or program"
  sys.exit()

# Checks to see if the document type is docx or csv
# regardless of case.
docx_type = re.search("docx", doc_type, flags=re.I)
csv_type = re.search("csv", doc_type, flags=re.I)

# Cannot handle any other document types besides csv or docx for now
if not docx_type and not csv_type:
  print "Error: Wrong document type given, use csv or docx"
  sys.exit()
  
# Outputs a schema'd JSON file for the file given
def output_JSON(file_path):
  # Generates a list of all documents matching the given
  # document type
  for doc in glob.glob(file_path):
    if docx_type:
      JSON_data = word.parse_text(doc,mode,schema)

    if csv_type:
      JSON_data = csv.parse_csv(doc,mode,schema)

    file_name = JSON_data[0]
    with open(file_name, 'w') as outfile:
     del JSON_data[0]
     json.dump(JSON_data, outfile, sort_keys = False, indent = 4, ensure_ascii=False)

output_JSON(file_path1)
output_JSON(file_path2)

