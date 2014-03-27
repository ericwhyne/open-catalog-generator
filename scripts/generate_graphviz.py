#!/usr/bin/python
import json
import re
import sys
import time
import os
import shutil
import darpa_open_catalog as doc
from pprint import pprint

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
build_dir = sys.argv[3]
darpa_links = sys.argv[4]
date = time.strftime("%Y-%m-%d", time.localtime())

print """
Active content file: %s
Data directory: %s
Build directory: %s
""" % (active_content_file, data_dir, build_dir)

print "Attempting to load %s" %  active_content_file
active_content = json.load(open(active_content_file))

for program in active_content:
  # program['Program Name']
  software_columns = []
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
    sys.exit(1)
  else:
    print "Attempting to load %s" %  program['Program File']
    program_details = json.load(open(data_dir + program['Program File']))

    animals:{'color':'red','shape':'rect','label':'Animals', link:'http://stackoverflow.com'},

    if re.search('^http',program_details['Link']):
      program_details['Link'] program_details['Long Name']
    else:
      program_details['Long Name']
    # program_details['Description']
    # program_details['Program Manager']
    # program_details['Program Manager Email'])
    
    
  # This creates a hashed array (dictionary) of teams that have publications. We use this to cross link to them from the software table.
  pubs_exist = {}
  if program['Pubs File'] != "" and program['Software File'] != "":
      print "Attempting to load %s" %  program['Pubs File']
      pubs_file = open(data_dir + program['Pubs File'])
      pubs = json.load(pubs_file)
      pubs_file.close()
      #print "Attempting to load %s" %  program['Software File']
      #softwares = json.load(open(data_dir + program['Software File'])) 
      for pub in pubs:
        for team in pub['Program Teams']:
          pubs_exist[team] = 1

 
  ###### SOFTWARE
  # ["Team","Software","Category","Code","Stats","Description","License"]
  if program['Software File'] != "":
    print "Attempting to load %s" %  program['Software File']
    softwares = json.load(open(data_dir + program['Software File']))   
     for software in softwares:
      for column in software_columns:
          for team in software['Program Teams']:
            if team in pubs_exist:
              team += " <a href='#" + team + "' onclick='pubSearch(this)'>(publications)</a>"
          software['Software']
          elink = software['External Link']
          if re.search('^http',elink) and elink != "":
            if darpa_links == "darpalinks":
              lurl = "http://www.darpa.mil/External_Link.aspx?url=" + elink
            else:
              lurl = elink
          else:
            # unlinked

####### Publications
  if program['Pubs File'] != "":
    print "Attempting to load %s" %  program['Pubs File']
    pubs = json.load(open(data_dir + program['Pubs File']))
    for pub in pubs:
      for team in pub['Program Teams']:
        # team
      link = pub['Link']
      if re.search('^http',link) or re.search('^ftp',link):
        if darpa_links == "darpalinks":
          lurl = "http://www.darpa.mil/External_Link.aspx?url=" + link
        else:
          lurl = link
      else:
        # not a link





























































