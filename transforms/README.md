# Introduction
The scripts **transform\_into\_JSON.py**, **word\_to\_JSON.py**, and **csv\_to\_JSON.py** all
try to help automate the process of converting information into the Open Catalog's 
JSON schemas.

# docx Files
docx files that contain publications can be parsed i.e. a list of academic references. See **ADAMS-scrubbed.docx** or **SMISC-scrubbed.docx** in the
**transforms** folder to see what a transformable document looks like.

## Proper Format
docx documents that are to be transformed must be formatted in a certain way to be parsed correctly.

### Titles/Headers
The first piece of text in the document must be the title of the reference list which should be
in the format:  
```
DARPA_Program Publications e.g. ADAMS Publications
```

Each set of publications by a particular program team must be separated by a header with the name:
```
Program_Team Publications e.g. IBM Publications.
```

### Authors
Authors should be separated by commas. The list of authors should end with a semicolon.
An example of this is below:  
```
Bader, D.A., Smith, J., and Bastion, J.;  
```
Other things to note about author names:
* The use of "and" or "&" in the list is perfectly fine.
* Names can come in many forms although the last name of an author
must be listed in full.
* Ensure that all names are separated with commas including the next to last name in the
list.
``` 
Right: George Costanza, and Darth Vader
Wrong: George Costanza and Darth Vader
```
* Ensure that the list ends with a semicolon and not any other punctuation mark.
```
Right: Simpson, H., Costanza, G., and Cosmo Kramer;
Wrong: Simpson, H., Costanza, G., and Cosmo Kramer,;
```

### Titles
The titles of publications must be enclosed in double quotes in order for the script to 
detect it.
```
"Gone with the wind"
```
The one thing to be wary of is non-ASCII quotes i.e. quotes that don't resemble **'** or **"**.
The word processor should allow you to turn off the replacement of ASCII quotes for non-ASCII quotes.

### Links
Links include any http or https URL. 

* Hyperlinked text will not suffice as the parser picks it up as regular text. Separate
the link from the text.
* The transform script will not check the validity of the URL, this must be done with another
script.

### Other
Erase useless information e.g. (Best Paper/Short Paper) in a title or a link as they mean nothing to the parser or user.

# csv Documents/Template Mode
Works for csv documents, and will essentially scan the master schema file, **00-schema-examples.json** 
, and use the schemas present with a csv document to produce a JSON file. 

## Template Mode Format
As a general rule of thumb, the csv document in question should follow the Excel template very closely but more
specific rules are below.

### Column Headers
Column headers should match the names in the **00-schema-examples.json** file so the script can match the appropriate
values to the JSON Schema. Below is an example of correct headers for the Publication schema.

**Right:**

| DARPA Program Name | Program Teams |
| --- | --- |
| XDATA | IBM, Data Tactics, Stanford |

**Wrong:**

| XDATA Program | Teams |
| --- | --- |
| XDATA | IBM, Data Tactics, Stanford |

Please check **00-schema-examples.json** or the Excel template if you are ensure of the proper header names.

### Multiple Values
In columns where multiple values are to be expected such as Authors in the Publication Schema, these values
should be separated by commas. Using newline characters will lead to incorrect parsing.

**Right:**

| Authors |
| --- |
| J. Query, J. Script |

**Wrong:**

| Authors |
| --- |
| J. Query and J. Script |

The above examples will lead to the following JSON results:

```
Right: "Authors": ["J. Query", "J. Script"]
Wrong: "Authors": ["J. Query and J. Script"]
```

### Punctuation
The values inside the csv columns are translated directly into JSON values which means double quotes
and newline characters as well. Double quotes should be removed which can easily be done by the
find/replace tool available in word processors such as **OpenOffice**. Newline characters shouldn't 
be used as the script does not use them to parse and it will show up in the JSON attribute. 

| Title |
| ----- |
| "Ender's Game" |

would be translated as:

```
"Title": "\"Ender's Game\""
```

### Script Usage
To use the JSON file generator, go into the **transforms** folder. Place any documents to be transformed in the **documents** folder.

Use the command below:
```
./transform_into_JSON.py [-h][-t] mode list_of_files

[] indicates that it is optional
-h will display a help menu which explains how to use the command
-t will indicate to use template mode although it will only work with
csv files.
```
**mode** needs to be **pubs**, **software**, or **program**.

**list_of_files** means the name of each file to be transformed separated by a space.
```
example.csv words.docx
```

file names with spaces in them must be enclosed by double quotes
``` 
"example file.csv"
```
**Note:** Only csv and docx files are supported for now.

The completed JSON file will be inside the **new_json** folder
inside the **transforms** folder.

Examples of correct usage are below:
(assuming that I am located in the transforms directory)
```
./transform_into_JSON.py -t pubs example.csv example2.csv
./transform_into_JSON.py program program-EXAMPLE.docx
./transform_into_JSON.py -h
```

This readme will be updated as the transform script changes.
