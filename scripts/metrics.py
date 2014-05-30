#!/usr/bin/python
#James Tobat, 2014
import json
import sys
import time
import matplotlib.pyplot as plt
import csv
import os.path

# Command line arguments and global constants
active_content_file = sys.argv[1]
deployed_content_file = sys.argv[2]
data_dir = sys.argv[3]
metric_log_dir = sys.argv[4]
date = time.strftime("%Y-%m-%d", time.localtime())
str_divider = "-" * 30

# Checks to see if the metric directory exits
# and if it doesn't, will create it.
if not os.path.exists(metric_log_dir):
    os.makedirs(metric_log_dir)

metric_log_file = metric_log_dir + "metrics.csv"

# Checks to see if the metrics file exists or not
# , and if it doesn't, it will create it.
if not os.path.isfile(metric_log_file):
  create_file = open(metric_log_file, 'w')
  create_file.close()


# Creates or appends a new file in the log.
def create_new_log(status, stored_metrics):
  
  # Will append to a csv document.
  # When the csv document is empty,
  # it will write column headers.
  with open(metric_log_file, 'a') as file:
    output = csv.writer(file)
    if status == 3:
      # column headers
      output.writerow(['Date','Active Programs','Active Projects','Active Publications'\
                       ,'Deployed Programs', 'Deployed Projects', 'Deployed Publications'\
                       ,'Active Records', 'Active Attributes', 'Deployed Records'\
                       ,'Deployed Attributes', 'Projects Per Active Program'\
                       ,'Publications Per Active Program', 'Projects Per Deployed Program'
                       ,'Publications Per Deployed Program', 'Release Date (Y)'])
    # Will write a new column to the end of the CSV file
    # with the information given in the array.
    output.writerow(stored_metrics)

  return

# updates the log when run on the same
# date and the values have changed.
def update_log(stored_metrics):
  date = stored_metrics[0]
  rows = []
  # Reads in all the old values from
  # the original file except for
  # the row that needs updating, it will
  # replace that row with the new values.
  with open(metric_log_file, 'r') as read_file:
    reader = csv.reader(read_file)
    
    for row in reader:
      if row[0] == date:
        rows.append(stored_metrics)
      else:
        rows.append(row)

  # Creates a new csv file with the same name
  # as the old one, and will replace it with
  # the same log lines and the updated log line.
  with open(metric_log_file, 'w') as write_file:
    writer = csv.writer(write_file)
    writer.writerows(rows)

  return


# Checks to see if a metric log for the specified date
# exists. Returns an integer status where 0 represents
# log not found, 1 represents log is found, 2 represents
# log is found but needs updating, and 3 represents that
# the log is empty.
def csv_log_exists(metric_log):
  status = 0
  counter = 0
  date = metric_log[0]
  with open(metric_log_file, 'r') as file:
    metric_file = csv.reader(file)
    for row in metric_file:
      counter += 1
      if row[0] == date:
        if row == metric_log:
          status = 1
        else:
          status = 2
        break

  # Indicates that the file is new
  # and has nothing written in it.
  if counter == 0:
    status = 3
  return status

# Returns the names of all programs that are currently
# deployed.
def programs_deployed():
  deployed_programs = []
  try:
    json_content = json.load(open(deployed_content_file))
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % file_name
    print " Details: %s" % str(e)
    sys.exit(1)
  
  for program in json_content:
    program_name = program['Program Name']
    deployed_programs.append(program_name)

  return deployed_programs

# Returns useful statistics for JSON files that list
# data about the various DARPA programs.
def gather_metrics(file_name, program_details):
  # Stores all useful metrics
  metrics = [0] * 5
  # Represents total attributes of all files scanned
  attributes = 0
  total_records = 0
  # Number of DARPA program
  programs = 0
  # Number of software/projects for the various
  # darpa programs for 1 program
  projects = 0
  # Number of publications for the various
  # darpa programs for 1 program
  pubs = 0
  total_pubs = 0
  total_projects = 0
  # Used to prevent the counting of attributes
  # for the same file, multiple times
  counter = 0
  # Number of attributes per record in the file presented
  num_attributes = 0
  
  # Attempts to load all JSON objects into a dictionary
  # and will throw an error if unsuccessful.
  try:
    json_content = json.load(open(file_name))
  except Exception, e:
    print "\nFAILED! JSON error in file %s" % file_name
    print " Details: %s" % str(e)
    sys.exit(1)
  deployed_programs = []
  if program_details:
    deployed_programs = programs_deployed()
    deployed_programs.sort()

  # For every darpa program in the file, it will compute
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

    # Tries to open the program JSON files for each program
    if program_file == "":
      print "ERROR: %s has no program details json file, can't continue. Please fix this and restart the build." % program_name
      sys.exit(1)
    else:
      program_metrics = json_metrics(program_file)
      attributes += program_metrics[1]
      total_records += program_metrics[0]
    
    # Tries to open the software JSON files for each program
    if project_file == "":
      projects = 0
    else:
      program_metrics = json_metrics(project_file)
      projects = program_metrics[0]
      attributes += program_metrics[1]
      total_records += program_metrics[0]
 
    # Tries to open the publication JSON files for each program
    if pub_file == "":
      pubs = 0
    else:
      program_metrics = json_metrics(pub_file)
      pubs = program_metrics[0]
      attributes += program_metrics[1]
      total_records += program_metrics[0]

    # Metrics for an individual program
    total_projects += projects
    total_pubs += pubs
    metrics[0] = program_name
    metrics[1] = projects
    metrics[2] = pubs

    # If details about each program are desired
    # it will then print out metrics for each
    # individual program. It will also state
    # if the program is deployed or not.
    if program_details:
      if program_name in deployed_programs:
        deployed = "Deployed"
      else:
        deployed = "Not Deployed"
      
      metrics[3] = deployed
      print_program(metrics)
  
  # Computes summary statistics for all programs given
  # in the JSON file.
  attributes += num_attributes * programs
  total_records += programs
  metrics[0] = total_records
  metrics[1] = attributes
  metrics[2] = programs
  metrics[3] = total_projects
  metrics[4] = total_pubs
  
  # Prints a divider only if there are
  # the code above printed out any metrics.
  if program_details:
    print str_divider

  return metrics

# Will print out useful information
# about each project.
def print_program(program_metrics):
  print "Program Name: %s" % program_metrics[0]
  print "Number of projects: %s" % program_metrics[1]
  print "Number of publications: %s" % program_metrics[2]
  print "Project Status: %s\n" % program_metrics[3]
  return

# will return the number of attributes a JSON record/object has
def count_attributes(json_record):
  num_attributes = 0
  for key, value in json_record.iteritems():
    num_attributes += 1
  
  return num_attributes

# Will return an array which includes the number of records/attributes
# in a JSON file, will work with either single or multiple JSON objects
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

# Places height of each bar on the
# bar graph
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

# Printout of summary statistics
print "\nProject Metrics:\n"
active_metrics = gather_metrics(active_content_file, True)
deployed_metrics = gather_metrics(deployed_content_file, False)
active_programs = active_metrics[2]
active_projects = active_metrics[3]
active_pubs = active_metrics[4]
deployed_programs = deployed_metrics[2]
deployed_projects = deployed_metrics[3]
deployed_pubs = deployed_metrics[4]
print "%s\n" % date
print "All Active Open Catalog Content:"
print "Number of Programs: %s" % active_programs
print "Number of Software Projects: %s" % active_projects
print "Number of Publications: %s\n" % active_pubs
print "All Deployed Open Catalog Content:"
print "Number of Programs: %s" % deployed_programs
print "Number of Software Projects: %s" % deployed_projects
print "Number of Publications: %s" % deployed_pubs
print str_divider

# misc metrics from the projects
print "Other Interesting Metrics:\n"
active_avg_projects = active_projects/active_programs
active_avg_pubs = active_pubs/active_programs
deployed_avg_projects = deployed_projects/deployed_programs
deployed_avg_pubs = deployed_pubs/deployed_programs
active_records = active_metrics[0]
active_attributes = active_metrics[1]
deployed_records = deployed_metrics[0]
deployed_attributes = deployed_metrics[1]
print "Average Number of Software Projects Per Active Program: %s" % active_avg_projects
print "Average Number of Publications Per Active Program: %s" % active_avg_pubs
print "Average Number of Software Projects Per Deployed Program: %s" % deployed_avg_projects
print "Average Number of Publications Per Deployed Program: %s" % deployed_avg_pubs
print "Active Content Records: %s" % active_records
print "Active Content Attributes: %s" % active_attributes
print "Deployed Content Records: %s" % deployed_records
print "Deployed Content Attributes: %s" % deployed_attributes
print str_divider

# Differences between the summary metrics of active and deployed
# content
print "Differences Between Active and Deployed Content:\n"
diff_records = active_records - deployed_records
diff_attributes = active_attributes - deployed_attributes
diff_programs = active_programs - deployed_programs
diff_projects = active_projects - deployed_projects
diff_pubs = active_pubs - deployed_pubs
print "Number of Records: %s" % diff_records
print "Number of Attributes: %s" % diff_attributes
print "Number of Programs: %s" % diff_programs
print "Number of Software Projects: %s" % diff_projects
print "Number of Publications: %s" % diff_pubs
print str_divider

# All information that is going to be stored in the log file.
# All fields must be strings in order to ensure that the log
# file is not updated needlessly.
stored_metrics = []
stored_metrics.append(date)
stored_metrics.append(str(active_programs))
stored_metrics.append(str(active_projects))
stored_metrics.append(str(active_pubs))
stored_metrics.append(str(deployed_programs))
stored_metrics.append(str(deployed_projects))
stored_metrics.append(str(deployed_pubs))
stored_metrics.append(str(active_records))
stored_metrics.append(str(active_attributes))
stored_metrics.append(str(deployed_records))
stored_metrics.append(str(deployed_attributes))
stored_metrics.append(str(active_avg_projects))
stored_metrics.append(str(active_avg_pubs))
stored_metrics.append(str(deployed_avg_projects))
stored_metrics.append(str(deployed_avg_pubs))

# Checks to see if the log for the date already exists.
# If it does exist, also checks to see if it needs updating.
# Also checks to see if the file is empty.
status = csv_log_exists(stored_metrics)
if status == 0 or status == 3:
  create_new_log(status, stored_metrics)
elif status == 2:
  update_log(stored_metrics)

# Will create a bar graph with the current metrics
# (number of pubs, projects, programs)
# of the deployed projects.
ind = [0] # location of the first bar
width = 1 # the width of the bars
y = [0 + width]
z = [0 + 2*width]
fig, ax = plt.subplots()
rects1 = ax.bar(ind, deployed_programs, width, color='r')
rects2 = ax.bar(y, deployed_projects, width, color='g')
rects3 = ax.bar(z, deployed_pubs, width, color='b')

# Labels the graph appropriately
ax.set_ylabel('Total Number')
ax.set_title('Deployed Project Metrics (Current)')
ax.set_xticks(ind)
ax.set_xticklabels('')
ax.legend( (rects1[0], rects2[0], rects3[0]), ('Programs', 'Projects', 'Publications'), loc='upper left' )
autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.show()