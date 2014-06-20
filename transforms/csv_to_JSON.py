#!/usr/bin/python
# James Tobat, 2014
import csv
import os
import re
import copy

# Parses a csv document in a mode (pub, project, program)
# using a schema that it can attach JSON information to.
# The end result is an array of JSON information which includes
# the document title as well as all the JSON records identified
# in the document (all use the schema passed in)
def parse_csv(document, mode, schema):
  i = 0
  JSON_Information = []
  document = os.path.basename(document)
  # Uses the name of the document given but replaces the file type
  # with JSON. This will be the name of the output file.
  doc_name = re.sub(".csv", ".json", document, flags=re.I)
  JSON_Information.append(doc_name)
  # Identifies the DARPA Program by removing
  # the schema name from the file name e.g.
  # HACM-pubs would change to HACM.
  # Assumes the title of the document contains the 
  # DARPA Program's name either in the form
  # DARPA_Program-schema_type.filetype e.g. HACM-pubs.csv
  # or is the name of the file itself e.g. PPAML.csv
  darpa_program = re.sub("-.*","",document)
  darpa_program = re.sub("\..*","",darpa_program)
  schema['DARPA Program'] = darpa_program
  #print doc_name
  
  with open(document, 'r') as read_file:
    reader = csv.reader(read_file)
    # With the first row, checks the column titles given
    # in order to identify which column maps to which schema
    # item
    initial_row = True
    team_index = -1
    title_index = -1
    link_index = -1
    project_index = -1
    category_index = -1
    code_index = -1
    home_index = -1
    description_index = -1
    license_index = -1

    for row in reader:
      if mode == "pub":
        if initial_row:
          initial_row = False
          i = 0
          # Maps the column titles to indices
          # which ensures that the script will
          # work even if the order changes
          for column in row:
            if column == "Team":
              team_index = i
              #print "team %i" % i
            if column == "Title":
              title_index = i
              #print "title %i" % i
            if column == "Link":
              link_index = i
              #print "link %i" % i
            i += 1
        else:
          #print row
          # Copies all relevant schema information
          # in a row to the JSON array.
          # Always uses a blank copy of the schema
          # to ensure that wrong information isn't 
          # copied.
          record = copy.deepcopy(schema)
          record['Title'] = row[title_index]
          record['Program Teams']=[row[team_index]]
          record['Link'] = row[link_index]
          JSON_Information.append(record)

      if mode == "project":
        if initial_row:
          initial_row = False
          i = 0
          # Maps the column titles to indices
          # which ensures that the script will
          # work even if the order changes
          for column in row:
            if column == "Team":
              team_index = i
            if column == "Project":
              project_index = i
            if column == "Category":
              category_index = i
            if column == "Code":
              code_index = i
            if column == "Public Homepage":
              home_index = i
            if column == "Description":
              description_index = i
            if column == "License":
              license_index = i
            i += 1
        else:
          # Copies all relevant schema information
          # in a row to the JSON array.
          # Always uses a blank copy of the schema
          # to ensure that wrong information isn't 
          # copied.
          record = copy.deepcopy(schema)
          record['Software'] = row[project_index]
          record['Program Teams']=[row[team_index]]
          record['External Link'] = row[home_index]
          record['Public Code Repo'] = row[code_index]
          record['Description'] = row[description_index]
          record['License'] = [row[license_index]]
 
          # Assumes the catagories of a project are seperated
          # by slashes e.g. Cloud/Cybersecurity/Big Data.
          # Will also trim non-important white space.
          categories = row[category_index].split('/')
          for j in xrange(len(categories)):
            category = categories[j]
            categories[j] = category.strip()
          record['Categories'] = categories

          JSON_Information.append(record)

  return JSON_Information

