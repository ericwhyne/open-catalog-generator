#!/usr/bin/python
#James Tobat, 2014
import json
import sys
import time
import os

active_content_file = sys.argv[1]
deployed_content_file = sys.argv[2]
data_dir = sys.argv[3]
date = time.strftime("%Y-%m-%d", time.localtime())
str_divider = "-" * 30

# Returns useful statistics for JSON files that list
# data about the various DARPA programs
def gather_metrics(file_name):
  # stores all useful metrics
  metrics = [0] * 5
  # represents total attributes of all files scanned
  attributes = 0
  total_records = 0
  # number of DARPA program
  programs = 0
  # number of software/projects for the various
  # darpa programs for 1 program
  projects = 0
  # number of publications for the various
  # darpa programs for 1 program
  pubs = 0
  total_pubs = 0
  total_projects = 0
  # used to prevent the overuse of a method
  counter = 0
  # number of attributes per record in the file presented
  num_attributes = 0
  

  try:
    json_content = json.load(open(file_name))
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % file_name
    print " Details: %s" % str(e)
    sys.exit(1)
  # for every darpa program in the file, it will compute
  # statistics for each one
  for program in json_content:
    if counter < 1:
      num_attributes = count_attributes(program)
      counter += 1
    program_name = program['Program Name']
    program_file = program['Program File']
    pub_file = program['Pubs File']
    project_file = program['Software File']
    programs += 1

    if program_file == "":
      print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
      sys.exit(1)
    else:
      program_metrics = json_metrics(program_file)
      attributes += program_metrics[1]
      total_records += program_metrics[0]
    # tries to open the software/publication files for each project
    # if it cannot 
    if project_file == "":
      projects = 0
    else:
      program_metrics = json_metrics(project_file)
      projects = program_metrics[0]
      attributes += program_metrics[1]
      total_records += program_metrics[0]

    if pub_file == "":
      pubs = 0
    else:
      program_metrics = json_metrics(pub_file)
      pubs = program_metrics[0]
      attributes += program_metrics[1]
      total_records += program_metrics[0]

    total_projects += projects
    total_pubs += pubs
    metrics[0] = program_name
    metrics[1] = projects
    metrics[2] = pubs
    print_program(metrics)
  
  attributes += num_attributes * programs
  total_records += programs
  metrics[0] = total_records
  metrics[1] = attributes
  metrics[2] = programs
  metrics[3] = total_projects
  metrics[4] = total_pubs
  print str_divider
  return metrics

# will print out useful
def print_program(program_metrics):
  print "Program Name: %s" % program_metrics[0]
  print "Number of projects: %s" % program_metrics[1]
  print "Number of publications: %s\n" % program_metrics[2]

  return

# will return the number of attributes a JSON record/object has
def count_attributes(json_record):
  num_attributes = 0
  for key, value in json_record.iteritems():
    num_attributes += 1
  
  return num_attributes

# will return an array which includes the number of records/attributes
# in a JSON file, will work with either for single or multiple JSON objects
def json_metrics(file_name):
  metrics = [0] * 2
  counter = 0
  records = 0
  file_path = data_dir + file_name

  try:
    json_content = json.load(open(file_path))
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % file_name
    print " Details: %s" % str(e)
    sys.exit(1)

  # Detects if the JSON object is either a single record
  # or an array of them
  if isinstance(json_content, dict):
    records = 1
    num_attributes = count_attributes(json_content)
  else:
    for record in json_content:
      if counter < 1:
        num_attributes = count_attributes(record)
        counter += 1
      records += 1

  attributes = records * num_attributes
  metrics[0] = records
  metrics[1] = attributes
  return metrics

# printout of summary statistics 
print "\nActive Content Project Metrics:\n"
active_metrics = gather_metrics(active_content_file)
print "\nDeployed Content Project Metrics:\n"
deployed_metrics = gather_metrics(deployed_content_file)

print "%s\n" % date
print "All Active Open Catalog Content:"
print "Number of Programs: %s" % active_metrics[2]
print "Number of Projects: %s" % active_metrics[3]
print "Number of Publications: %s\n" % active_metrics[4]
print "All Deployed Open Catalog Content:"
print "Number of Programs: %s" % deployed_metrics[2]
print "Number of Projects: %s" % deployed_metrics[3]
print "Number of Publications: %s" % deployed_metrics[4]
print str_divider

print "Other Interesting Metrics:\n"
print "Active Content Records: %s" % active_metrics[0]
print "Active Content Attributes: %s" % active_metrics[1]
print "Deployed Content Records: %s" % deployed_metrics[0]
print "Deployed Content Attributes: %s" % deployed_metrics[1]
total_attributes = active_metrics[1] + deployed_metrics[1]
total_records = active_metrics[0] + deployed_metrics[0]
print "Total Number of Records: %s" % total_records
print "Total Number of Attributes: %s" % total_attributes
print str_divider

print "Differences Between Active and Deployed Content:\n"
diff_records = active_metrics[1] - deployed_metrics[1]
diff_attributes = active_metrics[1] - deployed_metrics[1]
diff_programs = active_metrics[2] - deployed_metrics[2]
diff_projects = active_metrics[3] - deployed_metrics[3]
diff_pubs = active_metrics[4] - deployed_metrics[4]
print "Number of Records: %s" % diff_records
print "Number of Attributes: %s" % diff_attributes
print "Number of Programs: %s" % diff_programs
print "Number of Projects: %s" % diff_projects
print "Number of Publications: %s" % diff_pubs
print str_divider




