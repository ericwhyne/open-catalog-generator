#!/usr/bin/python
# James Tobat, 2014
try:
  from xml.etree.cElementTree import XML
except ImportError:
  from xml.etree.ElementTree import XML
import zipfile
import re
import copy

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

# The code for this function comes from Etienne Desautels
# Found on https://gist.github.com/7539105.git
# Extracts all text from a word document, will group
# text in paragraphs together but strange formatting
# such as hyperlinks will usually result in a seperate
# group of text.
def get_docx_text(path):
  document = zipfile.ZipFile(path)
  xml_content = document.read('word/document.xml')
  document.close()
  tree = XML(xml_content)
 
  paragraphs = []
  for paragraph in tree.getiterator(PARA):
    texts = [node.text
      for node in paragraph.getiterator(TEXT)
      if node.text]
    if texts:
      paragraphs.append(''.join(texts))
  return paragraphs

# Checks to see if a string is a url (http/https link)
# but does not check to see if the link actually works
def is_link(text):
  find_link = re.search("http[s]?://.*",text,re.I)
  if find_link:
    # seperates the html link from any text unrelated
    # to the link.
    http = find_link.group(0)
    link_split = http.split(' ')
    link = link_split[0]
  else:
    link = 0

  return link

# Checks to see if a piece of text contains the word
# publications. This indicates that the program
# team has changed or it is possibly the title.
def is_pub(text):
  find_pub = re.search(".* Publications", text, re.I)
  if find_pub:
    pub = find_pub.group(0)
    # Extracts the program team by removing the publications
    # word and any text after it.
    cleaned_pub = re.sub(" Publications.*", "", pub, flags=re.I)
  else:
    cleaned_pub = 0

  return cleaned_pub

# Identifies the names of authors inside of a string.
# Assumes the names of authors are seperated by commas
# and that the list of authors is closed off with a 
# semicolon e.g. Simpson, H. J., & Flanders, N.
def parse_names(text):
  # Seperates the list of authors from the rest of
  # the string
  find_names = re.search(".*;", text)
  authors = []
  
  # Parses the list of names if they are found
  if find_names:
    names = find_names.group(0)
    # and/& removed from list of authors.
    # Very common in literary references so they 
    # are automatically handled
    names_no_and = re.sub("and ", "", names, flags=re.I)
    names_clean = re.sub("& ", "", names_no_and, flags=re.I)
    # Removes the semicolon and all text unrelated to the names
    names_cleanest = re.sub(";.*", "", names_clean, flags=re.I)
    # Seperates the individual names/initials of all authors.
    names_list = names_cleanest.split(",")
    name_complete = True
    partial_name = ""
    full_name = ""
 
    for name in names_list:
      # Removes leading/trailing whitespace in names
      name = name.strip()
      # Finds the presence of an initial e.g. A.
      name_initial = re.findall("[A-Z]\.", name)
      # Finds the presence of an initial e.g. A
      name_initial_nodot = re.findall("[A-Z] ", name)
      # Finds full names e.g. Smith
      name_full = re.findall("[A-Z][a-zA-Z'\-]+", name)
      
      # Puts together a name that is spread across commas
      # typically consists of a last name, initials e.g.
      # Smith, A.
      # This will also reorder the name so Smith, A.
      # would be read out as A. Smith
      if not name_complete:
        full_name = name + " " + partial_name
        authors.append(full_name)
        name_complete = True
      else:
        # Number of initials in a string
        partial_names = len(name_initial) + len(name_initial_nodot)
        # Number of full names in a string
        whole_names = len(name_full)
        
        # If there is more than 1 whole name, or a combination
        # of whole names and initials, this incidates that there
        # is a complete name in the string e.g. H.J. Simpson 
        # or Ned Flanders
        if partial_names > 0 and whole_names > 0 or whole_names > 1:
           authors.append(name)
        else:
           # The first piece of a name
           # which is always the last name in literary
           # references.
           partial_name = name
           name_complete = False
    
    return authors
  else:
    return 0

# Identifies the title of a publication, assumes
# that the title is contained within double quotes
def is_title(text):
  find_title = re.findall("\"(.*?)\"", text, re.DOTALL)
  if find_title:
    return find_title[0]
  else:
    return 0

# Parses a word document in a mode (pub, project, program)
# using a schema that it can attach JSON information to.
# The end result is an array of JSON information which includes
# the document title as well as all the JSON records identified
# in the document (all use the schema passed in)
def parse_text(document, mode, schema):
  i = 0
  test = 0
  JSON_Information = []
  # Ensures that each copy of the schema
  # is blank
  JSON_record = copy.deepcopy(schema)
  no_link = False
  clear_record = False
  text = get_docx_text(document)

  for line in text:
    line = line.encode('ascii','ignore')
    if mode == "pubs":
      if i == 0:
        research_team = ""
      # Extracts useful pieces of the string
      team_name = is_pub(line)
      link = is_link(line)
      title = is_title(line)
      names = parse_names(line)

      if title:
        # If no link was found, appends the information
        # collected about the other parts of the schema.
        if no_link:
          #test += 1
          #print test
          JSON_Information.append(JSON_record) 
          JSON_record = copy.deepcopy(schema)
          JSON_record['DARPA Program'] = darpa_program
          JSON_record['Program Teams'] = [research_team]
        # If a link is found, then this will be set to false
        # to ensure that information isn't captured twice
        no_link = True
        JSON_record['Title'] = title

      if names:
       JSON_record['Authors'] = names
      
      # If a new program team is found, the schema
      # is updated appropriately. Assumes the sections
      # of publications are seperated by headers
      # stating the name of the program team.
      if team_name and not link:
        test = 0
        #print team_name
        if i == 0:
          darpa_program = copy.deepcopy(team_name)
          JSON_record['DARPA Program'] = darpa_program
          file_title = "%s-pubs.json" % team_name
          JSON_Information.append(file_title)    
        else:
          research_team = copy.deepcopy(team_name)
          JSON_record['Program Teams'] = [research_team]
      
      # Checks to see if a URL has been found, and then
      # will append all information gathered
      if link:
        test += 1
        #print test
        no_link = False
        JSON_record['Link'] = link
        JSON_Information.append(JSON_record) 
        JSON_record = copy.deepcopy(schema)
        JSON_record['DARPA Program'] = darpa_program
        JSON_record['Program Teams'] = [research_team]
      
    i+=1
  return JSON_Information

