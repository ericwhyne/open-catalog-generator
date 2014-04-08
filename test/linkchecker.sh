#!/bin/bash
linkchecker --file-output=html/$1 --recursion-level=2 --ignore-url='build\/stats\/' --no-warnings $2
