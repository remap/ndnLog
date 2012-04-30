ndnLog
================

scraper for ndn hubs to watch traffic over N nodes... made for ndnvideo testing in ec2, but could be used to monitor traffic along any hosts.

dependencies:

mongodb
apache
mod python
allowAccessDomain * in apache headers

description:
'aggregator.py' scrapes :9695 status pages into database. 
'database.py' formats data to json for display.
'monitor/display.html' is a basic plot of last data view.
'monitor/area.html' is a first pass at an area chart, showing 3 data parameters (first and last two)

usage:

aggregator.py must run on web host
visit monitor/display.html and/or monitor/area.html to see status


ToDo:

basic plotting is in place. 

taking it further will have to wait. ( a la http://mbostock.github.com/d3/ex/stream.html)