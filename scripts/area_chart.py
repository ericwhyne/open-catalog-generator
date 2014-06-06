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
        if row[release_index] == 'Y':
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

  # constructs an area chart that lists the deployed programs,
  # projects, and publications over time.
  fig = plt.figure()
  ax1 = fig.add_subplot(111)
  ax1.plot(p, programs, 'k^', p, projects, 'ko', p, pubs, 'kD', markersize = 8, linewidth = 0) 
  ax1.set_xticks(p)
  ax1.set_xticklabels(dates)
  ax1.fill_between(p, 0, x, facecolor="red")
  ax1.fill_between(p, x, y, facecolor="green")
  ax1.fill_between(p, y, z, facecolor="yellow")
  prog = plt.Rectangle((0,0), 1, 1, fc="red")
  proj = plt.Rectangle((0,0), 1, 1, fc="green")
  pub = plt.Rectangle((0,0), 1, 1, fc="yellow")
  ax1.legend([prog,proj,pub], ["Programs", "Projects", "Publications"], loc="upper center", ncol=3, bbox_to_anchor=(0.5,1.10))
  ax1.set_ylabel('Total Number')
  ax1.set_xlabel('Dates')

  for xpoint, ypoint in zip(p, programs):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  for xpoint, ypoint in zip(p, projects):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  for xpoint, ypoint in zip(p, pubs):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  ax1.axis([min(p) - 0.1, max(p) + 0.1, -1, max(pubs) + 50])

  plt.show()
=======
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
        if row[release_index] == 'Y':
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

  # constructs an area chart that lists the deployed programs,
  # projects, and publications over time.
  fig = plt.figure()
  ax1 = fig.add_subplot(111)
  ax1.plot(p, programs, 'k^', p, projects, 'ko', p, pubs, 'kD', markersize = 8, linewidth = 0) 
  ax1.set_xticks(p)
  ax1.set_xticklabels(dates)
  ax1.fill_between(p, 0, x, facecolor="red")
  ax1.fill_between(p, x, y, facecolor="green")
  ax1.fill_between(p, y, z, facecolor="yellow")
  prog = plt.Rectangle((0,0), 1, 1, fc="red")
  proj = plt.Rectangle((0,0), 1, 1, fc="green")
  pub = plt.Rectangle((0,0), 1, 1, fc="yellow")
  ax1.legend([prog,proj,pub], ["Programs", "Projects", "Publications"], loc="upper center", ncol=3, bbox_to_anchor=(0.5,1.10))
  ax1.set_ylabel('Total Number')
  ax1.set_xlabel('Dates')

  for xpoint, ypoint in zip(p, programs):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  for xpoint, ypoint in zip(p, projects):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  for xpoint, ypoint in zip(p, pubs):
    # Annotate the points 5 _points_ above and to the left of the vertex
    ax1.annotate('{}'.format(ypoint), xy=(xpoint, ypoint), xytext=(-5, 5), ha='center',
                textcoords='offset points')

  ax1.axis([min(p) - 0.1, max(p) + 0.1, -1, max(pubs) + 50])

  plt.show()

