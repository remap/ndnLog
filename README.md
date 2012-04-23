ndnLog
================

scraper for ndn hubs to watch traffic over N nodes... made for ndnvideo testing in ec2.

dependencies:

mongodb
apache
mod python
allowAccessDomain * in apache headers

description:
'aggregator.py' scrapes :9695 status pages into database. 
'monitor/display.html' requests json feed of latest values from database. 

usage:

aggregator.py must run on web host
visit monitor/display.html to see status


ToDo:

make the display plot / graph a la http://mbostock.github.com/d3/ex/stream.html