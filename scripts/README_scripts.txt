Author: James Tobat
Date: 6/24/2014
Summary: This is a README which describes the usage of the scripts that I have written in this folder.

Script: test-cross-site-scripting.py

Description: This script checks all JSON files in the data directory (darpa_open_catalog folder)
for embedded html tags. This script will not fix or replace any tags present nor will it differentiate
between harmless html tags such as <br> tags and harmful ones such as <script> tags. The script
will identify the document in which the html was found as well as a line and column number.

Usage: The command "make datatest" will run the script, but this assumes the darpa_open_catalog folder
with all the JSON data is already present.

Script: metrics.py

Description: This script will generate metrics from the JSON files in the open catalog. On the command line,
the script will spit out various statistics such as active programs/projects/publications and deployed
programs/projects/publications as well as others. It will also generate a csv file called metrics.csv inside
of the metrics_log folder that includes every statistic available on the command line. It will also include
a date stamp (it stores one log per day). If you run the script on the same day, but the stats change, the log
will replace the line with the updated stats.

Usage: The command "make metrics" will run the script, but this assumes the darpa_open_catalog folder
with all the JSON data is already present.

Script: area_chart.py

Description: This script will generate a stacked area graph from the metrics log from dates specified
as release dates. The graph specifically shows the number of deployed programs, projects, and publications
stacked on top of each other for each release date.

Usage: The command "make chart" will run the script. This assumes that the metrics log is already present
and that each appropriate row under the "Release Date (Y)" column is marked with a "y" or "Y". You must
have the python-matplotlib installed.

Script: category-condense.py

Description: This script will replace a value in the "Categories" section of all JSON files 
(except the schema example files) with a user supplied value. Basically, it is a find and
replace script for categories. This assumes the data directory (darpa_open_catalog) folder
is already there.

Usage: Once the terminal is inside the scripts folder, running the command
"./category-condenser.py word_to_replace replacement_word". word_to_replace
is the category keyword that needs to be replaced while the replacement_word
is the word that will replace all instances of the word_to_replace.

CAUTION: This script will replace the JSON files in the open catalog folder so
be cautious when running this script. If a mistake was made, you can re-run
the command but just reverse the order of the arguments.





