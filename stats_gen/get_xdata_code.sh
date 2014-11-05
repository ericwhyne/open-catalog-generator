#!/bin/bash
mkdir code
cat ../darpa_open_catalog/XDATA-software.json | ./jq '.[] | .["Public Code Repo"]' | grep -i '\.git\|github' | sed 's/\"//g' > code/gitrepos.txt
cat ../darpa_open_catalog/XDATA-software.json | ./jq '.[] | .["Public Code Repo"]' | grep -vi '\.git\|github' | sed 's/\"//g' > code/specialrepos.txt

#./_get_hard-to-get_code.sh &

cd code
cat gitrepos.txt | while read a; do git clone $a; done

echo -e "\n\n\nALL CODE IS FETCHED\n\n - Please reconcile code/specialrepos.txt with what was executed in _get_hard-to-get_code.sh to account for new exceptions.\n\n\n"
