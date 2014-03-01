#!/usr/bin/python
import json
import re
import sys
import darpa_open_catalog as doc
from pprint import pprint

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
build_dir = sys.argv[3]
darpa_links = sys.argv[4]

print """
Active content file: %s
Data directory: %s
Build directory: %s
""" % (active_content_file, data_dir, build_dir)

print "Attempting to load %s" %  active_content_file
active_content = json.load(open(active_content_file))

splash_page = doc.catalog_page_header()
splash_page += doc.logo()
splash_page += doc.catalog_splash_content()
splash_page += doc.splash_table_header()

for program in active_content:
  program_name = program['Program Name']
  program_page_filename = program_name + ".html"
  program_page = doc.catalog_page_header()
  if program['Program File'] == "":
    print "ERROR: %s has no program details json file, can't continue.  Please fix this and restart the build." % program_name
    sys.exit(1)
  else:
    print "Attempting to load %s" %  program['Program File']
    program_details = json.load(open(data_dir + program['Program File']))
    program_page += doc.logo()
    if re.search('^http',program_details['Link']):
      program_page += "  <h2><a href='" + program_details['Link'] + "' class='programlink'>" + program_details['Long Name'] + "</a></h2>\n"
    else:
      program_page += "<h2>%s</h2>" % program_details['Long Name']
    program_page += "<p>%s<p>" % program_details['Description']
    program_page += "<p>Program Manager: %s<p>" % program_details['Project Manager']
    program_page += "<p>Contact: %s<p>" % program_details['Project Manager contact']
    program_page += "<p>The DARPA Open Catalog adds links to external pages for software and publications as they are approved for public release. Software includes links to external project pages, and, where applicable, the code repository for the project. Publications link out to the published locations or indicate where publication is expected.</p>"
    splash_page += "<TR>\n <TD><a href='%s'>%s</a></TD>\n <TD>%s</TD>\n</TR>" % (program_page_filename, program_details['DARPA Program Name'], program_details['Description'])  

  
  if program['Software File'] != "":
    program_page += "<h2>Software:</h2>"
    print "Attempting to load %s" %  program['Software File']
    softwares = json.load(open(data_dir + program['Software File']))
    program_page += doc.software_table_header()
    for software in softwares:
      program_page += "<TR>\n  <TD>"
      for team in software['Program Teams']:
        program_page += team + ", "
      program_page = program_page[:-2]
      program_page += "</TD>\n "
      elink = ""
      if 'External Link' in software.keys():
        elink = software['External Link']
      if re.search('^http',elink) and elink != "":
        if darpa_links == "darpalinks":
          program_page += "  <TD><a href='http://www.darpa.mil/External_Link.aspx?url=" + elink + "'>" + software['Software'] + "</a></TD>\n"
        else:
          program_page += "  <TD><a href='" + elink + "'>" + software['Software'] + "</a></TD>\n"
      else:
        program_page += "  <TD>" + software['Software'] + "</TD>\n"

      categories = ""
      if 'Categories' in software.keys():
        for category in software['Categories']:
          categories += category + ", "
        categories = categories[:-2]
      program_page += "  <TD>" + categories + "</TD>\n"

#      instructional_material = ""
#      if 'Instructional Material' in software.keys():
#        instructional_material = software['Instructional Material']
#      if re.search('^http',instructional_material):
#        if darpa_links == "darpalinks":
#          program_page += "  <TD><a href='http://www.darpa.mil/External_Link.aspx?url=" + instructional_material + "'> Documenation or Tutorial </a></TD>\n"
#        else:
#          program_page += "  <TD><a href='" + instructional_material + "'> Documenation or Tutorial </a></TD>\n"
#      else:
#        program_page += "  <TD>" + instructional_material + "</TD>\n"

      clink = ""
      if 'Public Code Repo' in software.keys():
        clink = software['Public Code Repo']
      program_page += "  <TD> " + clink + " </TD>\n"

      program_page += " <TD> " + software['Description'] + " </TD>\n"
      
      program_page += " <TD> " + software['License'] + " </TD>\n </TR>\n"
    program_page += doc.software_table_footer()

  if program['Pubs File'] != "":
    print "Attempting to load %s" %  program['Pubs File']
    pubs = json.load(open(data_dir + program['Pubs File']))
    program_page += doc.pubs_table_header()
    for pub in pubs:
      program_page += "<TR>\n  <TD>"
      for team in pub['Program Teams']:
        program_page += team + "<a name='" + team + "'>, "
      program_page = program_page[:-2]
      program_page += "</TD>\n  <TD>" + pub['Title'] + "</TD>\n"
      link = pub['Link']
      if re.search('^http',link):
        if darpa_links == "darpalinks":
          program_page += "  <TD><a href='http://www.darpa.mil/External_Link.aspx?url=" + link + "'>" + link + "</a></TD>\n"
        else:
          program_page += "  <TD><a href='" + link + "'>" + link + "</a></TD>\n"
      else:
        program_page += "  <TD>" + link + "</TD>\n"
      program_page += "</TR>\n"
    program_page += doc.pubs_table_footer()

  program_page += doc.catalog_page_footer()
  print "Writing to %s" % build_dir + '/' + program_page_filename
  program_outfile = open(build_dir + '/' + program_page_filename, 'w')
  program_outfile.write(program_page)

splash_page += doc.splash_table_footer()
splash_page += doc.catalog_page_footer()

splash_page_file = build_dir + '/index.html'
print "Writing to %s" % splash_page_file
splash_outfile = open(splash_page_file, 'w')
splash_outfile.write(splash_page)





























































