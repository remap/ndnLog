import xml
import json
import urllib
from BeautifulSoup import BeautifulSoup
import config as cfg
import time
from decimal import *
import database as data

# respond to http query for data w/ json object


# yet first, lets make sure we can get the data

#print data.getLastEntry()

print data.getLastForEachHost()