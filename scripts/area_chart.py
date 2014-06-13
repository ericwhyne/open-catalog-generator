#!/usr/bin/python
#James Tobat, 2014
import matplotlib.pyplot as plt
import csv
import sys

metric_log_file = sys.argv[1]
programs = []
projects = []
pubs = []
dates = []

def add_array(list1, list2):
  i = 0
  new_list = []
  
  for value in list1:
    new_value = value + list2[i]
    i += 1
    new_list.append(new_value)
  
  return new_list

# reads in the metrics log and will
# gather all appropriate metrics
# for the deployed programs
with open(metric_log_file, 'r') as read_file:
  reader = csv.reader(read_file)
  counter = 0
  date_index = 0
  release_index = 0
  program_index = 0
  project_index = 0
  pub_index = 0

  for row in reader:
  
    if counter == 0:
      i = 0
      # find the index values for each of the
      # required columns in the csv, done to
      # ensure that if the log ever changes
      # it will still find the info.
      for value in row:
        if value == 'Date':
          date_index = i
        elif value == 'Deployed Programs':
          program_index = i
        elif value == 'Deployed Projects':
          project_index = i
        elif value == 'Deployed Publications':
          pub_index = i
        elif value == 'Release Date (Y)':
          release_index = i
        i += 1
    else:
      if len(row) >= release_index + 1:
        if row[release_index] == 'Y' or row[release_index] == 'y':
          dates.append(row[date_index])
          programs.append(int(row[program_index]))
          projects.append(int(row[project_index]))
          pubs.append(int(row[pub_index]))
    counter += 1

# will not graph data if there is only one point of it
if not len(dates) < 2:
  p = range(len(dates))

  x = programs
  y = projects
  z = pubs
  
  project_y = add_array(x,y)
  pub_z = add_array(project_y,z)

  # constructs an area chart that lists the deployed programs,
  # projects, and publications over time.
  fig = plt.figure()
  ax1 = fig.add_subplot(111)
  ax1.plot(p, programs, 'k^', p, project_y, 'ko', p, pub_z, 'kD', markersize = 8, linewidth = 0) 
  ax1.set_xticks(p)
  ax1.set_xticklabels(dates)
  ax1.fill_between(p, 0, x, facecolor="red")
  ax1.fill_between(p, x, project_y , facecolor="green")
  ax1.fill_between(p, project_y, pub_z, facecolor="yellow")
  prog = plt.Rectangle((0,0), 1, 1, fc="red")
  proj = plt.Rectangle((0,0), 1, 1, fc="green")
  pub = plt.Rectangle((0,0), 1, 1, fc="yellow")
  ax1.legend([prog,proj,pub], ["Programs", "Projects", "Publications"], loc="upper center", ncol=3, bbox_to_anchor=(0.5,1.10))
  ax1.set_ylabel('Total Number')
  ax1.set_xlabel('Dates')

  ax1.axis([min(p) - 0.1, max(p) + 0.1, -1, max(pub_z) + 100])

  plt.show()

