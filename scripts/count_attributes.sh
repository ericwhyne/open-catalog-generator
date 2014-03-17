#!/bin/bash
cd ../darpa_open_catalog/
cat $1*.json | sed '/^[{}].*$/d' | wc -l
