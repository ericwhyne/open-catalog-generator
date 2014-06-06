#!/bin/bash
cd code

mkdir immersive_body-based_interactions ; cd immersive_body-based_interactions
git svn init -s http://svnmimir.googlecode.com/svn/ ; git svn fetch &
cd ..

mkdir oodt ; cd oodt
git svn init -s https://svn.apache.org/repos/asf/oodt/ ; git svn fetch &
cd ..

mkdir bigdata ; cd bigdata
#git svn init -s https://bigdata.svn.sourceforge.net/svnroot/bigdata/ ; git svn fetch &
git svn init -s https://svn.code.sf.net/p/bigdata/code/ ; git svn fetch &
cd ..

mkdir mpgraph; cd mpgraph
git svn init -s http://svn.code.sf.net/p/mpgraph/code/ ; git svn fetch &
cd ..
