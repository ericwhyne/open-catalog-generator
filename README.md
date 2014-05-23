open-catalog-generator
======================

Code and templates required to build the DARPA open catalog.

add_json_fields.py
=========================
Steps for adding json fields to a specific file type:

1. Open the json file for the program that needs to be added or modified. Add a blank("") entry to the program json for both the "Display Software Columns" and "Display Pubs Columns" fields. See the following example:

    "Display Software Columns":[
        "Team",
        "Project",
		"",
        "Category",
        "Code",
        "Description",
        "License"
    ],
    "Display Pubs Columns":[
        "Team",
        "Title",
		"",
        "Link"
    ],

2. From the scripts directory, open the add_json_fields.py script in an editor. 

3. There are three variables to adjust(files_to_change, fields_to_add, insert_after) depending on the field and file specifications.
  3a. files_to_change: This variable should contain only the files that you wish to add fields to. The values can be "program", "software" and "pubs"
  3b. fields_to_add: This variable is a key-value pair object that takes the field name as the key and the field value as the value. There is no limit to the number of key-value pairs that can be added.
  3c. insert_after: The added field will be placed after the given field name
 
4. The Makefile contains a executable definition that can be used to quickly run this script after adjusting the two variables. Using the CYGWIN command line, run the following command "make addjsonfields"

5. Verify that the fields were added correctly and to the appropriate files by reviewing the new files in the "darpa_open_catalog/new_json" directory. If the files are correct, move them to the "darpa_open_catalog" directory and done! Now there are new json files for the next build!

6. Be sure to delete the "new_json" directory from the "darpa_open_catalog" directory so that it is not mistakenly committed to the project repository. 

Note: The json files that are reproduced are based on the active_content.json file. Be sure to add all of the json files that are to be reproduced to the active_content.json file before running the addjsonfields script.


convert_non_ascii_chars.py
=========================
Steps for converting/removing non-ascii characters from json files:

1. In the "darpa_open_catalog" directory, record the name of the file(s) that include non-ascii characters. 

2. From the scripts directory, open the convert_non_ascii_chars.py script in an editor and enter the name of the file(s) in the "files_to_fix" variable. See the following example:

   files_to_fix = ["CRASH-program.json", "CRASH-pubs.json"]
 
3. The Makefile contains a executable definition that can be used to quickly run this script after modifying the variable. Using the CYGWIN command line, run the following command "make allascii"

4. Verify that the non-ascii characters were replaced/removed by opening the new files in the "darpa_open_catalog/new_json" directory. If the files are correct, move them to the "darpa_open_catalog" directory and done! Now there are new json files for the next build!

5. Be sure to delete the "new_json" directory from the "darpa_open_catalog" directory so that it is not mistakenly committed to the project repository. 

Note: In some cases, a non-ascii character may not be mapped to an ascii character, therefore causing the character to be replaced with another non-ascii character or removed completely. If the character needs an ascii equivalent, an exception will need to be added to the "hex2ascii" method in the script to identify an ascii character to replace the character.

  def hex2ascii(hex):
    uni_num = int(hex,16)
    #print "uni_num: %s \r" % uni_num 
    if uni_num > 127:
      if uni_num == 8243:
        char_out = '"'
		.
		.
		.