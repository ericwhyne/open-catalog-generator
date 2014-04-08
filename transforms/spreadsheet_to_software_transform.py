#!/usr/bin/python
# 2013 Eric Whyne 
# http://www.datamungeblog.com
import json
import re
from pprint import pprint
import sys, getopt

lines = sys.stdin.readlines()

outtext = "[\n"
for line in lines:
  line =  re.sub('["\n]','',line)
  cells = line.split('~')
  teams = []
  teams.append(cells[0].encode('ascii', 'ignore').strip())
  software = cells[1].encode('ascii', 'ignore').strip()  

  categories = []
  categories.append(cells[7].encode('ascii', 'ignore').strip())
  imat = cells[2]
  code = cells[3]
  desc = cells[5]
  lic = cells[6]

  outtext+= "{\n"
  outtext+= "  \"DARPA Program\":\"" + "CFT" + "\",\n"

  outtext += "  \"Program Teams\":[" 
  for team in teams:
    outtext += "\"" + team.encode('ascii', 'ignore').strip() + "\","
  outtext = outtext[:-1] + "],\n"

  outtext+= "  \"Software\":\"" + software + "\",\n"

  outtext+= "  \"Public Code Repo\":\"" + code + "\",\n"

  outtext+= "  \"Description\":\"" + desc + "\",\n"

  outtext+= "  \"License\":\"" + lic + "\",\n"

  outtext+= "  \"Categories\":["
  for category in categories:
    outtext += "\"" + category.encode('ascii', 'ignore').strip() + "\","
  outtext = outtext[:-1] + "]\n"



  outtext+= "},\n"
outtext = outtext[:-2] + "\n]\n"

sys.stdout.write(outtext)

