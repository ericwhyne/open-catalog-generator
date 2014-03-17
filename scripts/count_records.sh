#!/bin/bash
cd ../darpa_open_catalog/
cat $1*.json | grep { | wc -l
