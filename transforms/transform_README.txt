Author: James Tobat
Date:6/20/14

This is a README on the usage of the transform scripts in this folder.

The scripts transform_into_JSON.py, word_to_JSON.py, and csv_to_JSON.py all
try to help automate the process of converting information into the open catalog's 
JSON schema.

docx files:
For word documents, it can parse publications but it must be in a similar format to the
documents that I originally parsed. See ADAMS-scrubbed.docx or SMISC-scrubbed.docx for an 
example of a correctly parsable document.

The first piece of text in the document must be the title of the reference list which should be
in the format "DARPA_Program Publications" e.g. ADAMS Publications

Each set of publications by a particular program team must be seperated by a header with the name 
"Program_Team Publications" e.g. IBM Publications.

The references themselves must have this format regardless of standard (APA/MLA/etc) used:

Authors:
Authors should be seperated by commas. The list of authors should end with a semicolon.
e.g. Bader, D.A., Smith, J., and Bastion, J.

-The use of "and" or "&" in the list is perfectly fine.
-Names can come in the form of "Last_Name, First_Name/Initials" or "First_Name Last_Name"
e.g. Skywalker, L. or Homer Simpson.
-Ensure that all names are seperated with commas including the next to last name in the
list e.g. Bob Barker and Darth Vader is wrong, it should be Bob Barker, and Darth Vader
-Ensure that the list ends with a semicolon and not any other punctuation mark
e.g. Simpson, H., Costanza, G., and Cosmo Kramer; - Right
e.g. Simpson, H., Costanza, G., and Cosmo Kramer,; - Wrong

Titles:
The titles of publications must be enclosed in double quotes in order for the script to 
detect it e.g. "Gone with the wind"

- The one thing to be wary of is non-ASCII quotes i.e. quotes that don't resemble ' or ".
The word processor should allow you to turn off the replacement of ascii quotes for non-ascii quotes
i.e. the quotes that face a direction depending on whether it is af the front or back of a word.

Links:
Links include any http or https URL. 

-Hyperlinked text will not suffice as the parser picks it up as regular text. Seperate
the link from the text.
-The transform script will not check the validity of the URL, this must be done with another
script.

References in general:
-Erase useless information e.g. (Best Paper/Short Paper) in a title or a link as they mean nothing to the parser or user.

csv Documents:
For csv documents, the format is a little more straightforward. All columns in the document should have headers and
then the corresponding values for that field per each row. The name of the csv file must inlude the DARPA program name
in either of these forms:

DAPRA_Program-schema_type.file_type e.g. HACMS-pubs.csv
DARPA_Program.file_type e.g. ADAMS.csv

The JSON file will have the exact same name as the csv file name.

Note:
The exact value (exluding needless whitespace) of a column will be replicated in the JSON file which includes 
newline characters or other erroneous information.

Script Usage:
To use the JSON file generator, go into the transforms file. 

Use the command below:
./transform_into_JSON.py doc_type mode

doc_type for now includes docx or csv

mode includes "pub" or "project" for now

Move a file that you want transformed into
the transforms folder. Be careful, it will transform
every document of the given type in the folder which could
lead to incorrect JSON files.

An example of correct usage is below:
(assuming that I am located in the transforms directory)
./transform_into_JSON.py docx pub
./transform_into_JSON.py csv project

This readme will be updated as the transform script changes.





