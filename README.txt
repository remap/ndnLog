ndnLog
================

scraper for ndn hubs to watch traffic over N nodes... made for ndnvideo testing in ec2, but could be used to monitor traffic along any hosts… perhaps we'll use something for the ndnnodes themselves.

dependencies:

mongodb
apache
mod python
allowAccessDomain * in apache headers

description:
'aggregator.py' scrapes :9695 status pages into database. 
'database.py' formats data to json for display.
'monitor/display.html' is a basic plot of last data view.
'monitor/area.html' is a first pass at an area chart, showing 3 hosts. 

usage:

aggregator.py must run on web host to create data
visit monitor/display.html and/or monitor/area.html to see status based on data


ToDo:

dynamic host list
	right now, all hostnames are in config (which is fine for borges, hydra, etc) - but not for ec2 instances. 

realtime display
	right now, the aggregate/historic is displaying. 
	The UI refreshes every N seconds, but the 'update' function for the chart requires 1:1 data mapping. 
	thus we cannot give new datapoints; simply update the old ones… so realtime will require some filter / 'framebuffer' / data abstraction

ideally we could have some fancy per-namespace (per-app) chart like http://mbostock.github.com/d3/ex/stream.html