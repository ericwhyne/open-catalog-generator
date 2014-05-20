open-catalog-generator
======================

Code and templates required to build the DARPA open catalog.

add_json_fields.py script
=========================
Steps to adding json fields to a specific file type:

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

2. Open the add_json_fields.py script in the script directory with an editor. 

3. There are three variables to adjust(files_to_change, fields_to_add, insert_after) depending on the field and file specifications.
  3a. files_to_change: This variable should contain only the files that you wish to add fields to. The values can be "program", "software" and "pubs"
  3b. fields_to_add: This variable is a key-value pair object that takes the field name as the key and the field value as the value. There is no limit to the number of key-value pairs that can be added.
  3c. insert_after: The added field will be placed after the given field name
 
4. The Makefile contains a executable definition that can be used to quickly run this script after adjusting the two variables. On the cygwin command line, run the following command "make addjsonfields"

5. Verify that the fields were added correctly and to the appropriate files by opening the "new_json" directory in the "darpa_open_catalog" directory. If the files are correct, move them to the "darpa_open_catalog" directory and done! Now there are new json files for the next build!

6. Be sure to delete the "new_json" directory from the "darpa_open_catalog" directory so that it is not mistakenly committed to the project repository. 

#Note: The json files that are reproduced are based on the active_content.json file. Be sure to add all of the json files that are to be reproduced to the active_content.json file before running the addjsonfields script.