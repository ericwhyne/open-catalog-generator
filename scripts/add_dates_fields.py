#!/usr/bin/python
import json
import re
import sys
import time
import os
import shutil
import darpa_open_catalog as doc
import sunburst_graphics as graph
from pprint import pprint

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
date = time.strftime("%Y-%m-%d", time.localtime())

print """
Active content file: %s
Data directory: %s
""" % (active_content_file, data_dir)

#To run script: ./scripts/add_dates_fields.py active_content.json /home/.../open-catalog-generator/darpa_open_catalog/


try:
  active_content = json.load(open(active_content_file))
except Exception, e:
  print "\nFAILED! JSON error in file 1 %s" % active_content_file
  print " Details: %s" % str(e)
  sys.exit(1)
  
for program in active_content:
  program_name = program['Program Name']
  print "Program %s \n" % program_name
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
    sys.exit(1)
  else:
    if program['Software File'] != "":
      try:
        orig_software_file = data_dir + program['Software File']
        software = json.load(open(orig_software_file))
        for sw in software:
          sw["New Date"] = ""
          sw["Update Date"] = ""
        new_software = json.dumps(software, indent=2);
        new_software_file = data_dir + program_name + '-software-withdates.json'
        print "Writing to %s \n" % new_software_file
        software_outfile = open(new_software_file, 'w')
        print "out file %s \n" % software_outfile
        software_outfile.write(new_software)  
      except Exception, e:
        print "\nFAILED! JSON error in file 2 %s" % program['Software File']
        print " Details: %s" % str(e)
        sys.exit(1)
    if program['Pubs File'] != "":
      try:
        pubs = json.load(open(data_dir + program['Pubs File']))
        for pub in pubs:	  
          pub["New Date"] = ""
          pub["Update Date"] = ""	  
        new_pubs = json.dumps(pubs, indent=2); 
        pubs_file = data_dir + program_name + '-pubs-withdates.json'
        print "Writing to %s" % pubs_file
        pubs_outfile = open(pubs_file, 'w')
        print "out file %s \n" % pubs_outfile
        pubs_outfile.write(new_pubs)	  
      except Exception, e:
        print "\nFAILED! JSON error in file 3 %s" % program['Pubs File']
        print " Details: %s" % str(e)
        sys.exit(1)