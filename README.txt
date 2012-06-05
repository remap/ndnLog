ndnLog
================

scraper for ndn hubs to watch traffic over N nodes... made for ndnvideo testing in ec2, but could be used to monitor traffic along any hosts.
perhaps we'll use something for the ndn nodes themselves?

usage:

visit control.html* to start/stop log & ec2 instances. 

* http://borges.metwi.ucla.edu/ec2/ndnLog/control.html

specific control steps:
1) log, press 'reset'
2) log, press 'start'
3) cloud, select desired instance count
4) cloud, press 'start'
then, when done:
5) cloud, press 'stop'
6) log, press 'stop'

visit monitor/area.html* to see status based on NDN Content Objects

* http://borges.metwi.ucla.edu/ec2/ndnLog/monitor/area.html

ToDo:

fix zero at beginning
add monitor/areaInterests.html to see status based on NDN Interest Packets

ideally we could have some fancy per-namespace (per-app) chart like http://mbostock.github.com/d3/ex/stream.html



install dependencies:

mongodb
apache
mod python
allowAccessDomain * in apache headers (for ajax data load across all browsers)

description:
'aggregator.py' scrapes :9695 status pages into database. 
'database.py' formats data to json for display.
'monitor/display.html' is a basic plot of last data view.
'monitor/area.html' is an area chart of traffic.