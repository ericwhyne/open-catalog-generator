#!/bin/bash
grep --color='auto' -P -n "[\x80-\xFF]" ../darpa_open_catalog/*.json 
