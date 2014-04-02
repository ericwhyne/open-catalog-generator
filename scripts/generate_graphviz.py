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

nodes = {}
edges = {}
nodes['DARPA'] = {'type':"agency",'color':'blue','shape':'rect','label':'DARPA'}

#print "Attempting to load %s" %  active_content_file
active_content = json.load(open(active_content_file))

for program in active_content:
  software_columns = []
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file." % program_name
    sys.exit(1)
  else:
    #print "Attempting to load %s" %  program['Program File']
    program_details = json.load(open(data_dir + program['Program File']))

  #print " NODE " + program_details['Long Name']
  nodes[str(program_details['Long Name'])] = {'type':"program",'color':'gray','shape':'rect','label':str(program_details['Long Name'])}
  nodes[str(program_details['Program Manager'])] = {'type':"pm",'color':'green','shape':'rect','label':str(program_details['Program Manager'])}
  edges[str(program_details['Long Name'])] = {str(program_details['Program Manager']):{}, 'DARPA':{}}
  # program_details['Description']
  # program_details['Program Manager']
  # program_details['Program Manager Email'])

  ###### SOFTWARE
  if program['Software File'] != "":
    #print "Attempting to load %s" %  program['Software File']
    softwares = json.load(open(data_dir + program['Software File']))   
    for software in softwares:
      nodes[str(software['Software'])] = {'type':"software",'color':'red','shape':'rect','label':str(software['Software'])}
      edges[str(software['Software'])] = {str(program_details['Long Name']):{}}
      # software['External Link']
      #for team in software['Program Teams']:
        #if team in pubs_exist:
          #team = "haspubs" # placeholder
        
  ####### Publications
  if program['Pubs File'] != "":
    #print "Attempting to load %s" %  program['Pubs File']
    pubs = json.load(open(data_dir + program['Pubs File']))
    for pub in pubs:
      nodes[str(pub['Title'])] = {'type':"pub",'color':'orange','shape':'rect','label':str(software['Software'])}
      edges[str(pub['Title'])] = {str(program_details['Long Name']):{}}
      # pub['Link']      
      #for team in pub['Program Teams']:
        


print "nodes:" + str(nodes) + ","
print "edges:" + str(edges)




























































