#!/bin/bash
directory="darpa_open_catalog"
starting_programs=1
starting_projects=72
starting_pubs=116
cd ../$directory/
programs=$(find -name \*-program.json | wc -l)
pubs=$(cat *-pubs.json | grep { | wc -l)
projects=$(cat *-software.json | grep { | wc -l)

echo "Kickoff:"
echo "$starting_programs program"
echo "$starting_projects projects"
echo -e "$starting_pubs publications\n"
echo -e "Current:\n$programs programs\n$projects projects\n$pubs publications\n"

program_diff=$(($programs-$starting_programs))
pub_diff=$(($pubs-$starting_pubs))
project_diff=$(($projects-$starting_projects))

echo -e "Differences:\n$program_diff programs\n$project_diff projects\n$pub_diff publications\n"
