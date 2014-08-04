#!/usr/bin/python
import json
import re
import sys
import unicodedata
import binascii
import chardet

active_content_file = sys.argv[1]
data_dir = sys.argv[2]
new_json_dir = sys.argv[3]
files_to_fix = []
files = ""

if len(sys.argv) > 3:
  files = re.split('\,',sys.argv[4])

  for i in range(0, len(files)):
    #print 'i in loop:', i
    files_to_fix.append(files[i])

print """
Active content file: %s
Data directory: %s
New JSON directory: %s
Files to convert: %s
""" % (active_content_file, data_dir, new_json_dir, files_to_fix)

def hex2ascii(hex):
  uni_num = int(hex,16)
  #print "uni_num: %s \r" % uni_num 
  if uni_num > 127:
    if uni_num == 8243:
      char_out = '"'
    elif uni_num == 8901:
      char_out = '.'	
    else:
      char_out = unichr(uni_num)
  else: 
    char_out = chr(uni_num)
  return char_out

def to_bytes(t, nbytes):
    #Format text t as a sequence of nbyte long values separated by spaces
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    num_chunks = len(hex_version) / chars_per_item
    def chunkify():
        for start in xrange(0, len(hex_version), chars_per_item):
            yield hex_version[start:start + chars_per_item]
    return ' '.join(chunkify())
 
try:
  for file in files_to_fix:
    json_file = open(data_dir + file)
    raw_string = json_file.read()	
    for m in re.finditer(r"[^\x00-\x7F]+", raw_string):
      print to_bytes(m.group(), 1) #char in bytes
      utf_literal = json.dumps(m.group(), ensure_ascii=False)
      print "utf-8 literal before conversion: %s" % utf_literal 
      normalize_char = unicodedata.normalize('NFKD', utf_literal.decode('utf-8')).encode('ascii','ignore')
      normalize_char = re.sub(r'^"|"$', '', normalize_char)
      final_conversion = ''
      if normalize_char == '':
        code_point = json.dumps(m.group(), ensure_ascii=True)
        hex_code = code_point.replace('\u','0x').strip('\n').replace('\"','')  
        final_conversion = hex2ascii(hex_code)
      else:
        final_conversion = normalize_char;
      print "ascii character after conversion: %s \n\r" % final_conversion
      raw_string = raw_string.replace(m.group(), final_conversion.encode('ascii','ignore'))
    try:
      new_json_file = new_json_dir + file
      print "Writing to %s \n" % new_json_file
      json_outfile = open(new_json_file, 'w')
      json_outfile.write(raw_string)
    except Exception, e:
      print "\nFAILED! Could not create new %s" % (file)
      print " Details: %s" % str(e)
      sys.exit(1)
except Exception, e:
  print "\nFAILED! JSON error in file %s" % file
  print " Details: %s" % str(e)
  sys.exit(1)
  
