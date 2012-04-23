import xml
import json
import urllib
from BeautifulSoup import BeautifulSoup
import config as cfg
import time
from decimal import *
import database as data

while True:
    time.sleep(cfg.loopDelay)
    for URI in cfg.URIs:
    	try:
        	status = urllib.urlopen(URI)
        	statusXML = status.read()
        	soup = BeautifulSoup(statusXML)
        except:
        	print "there is a problem, one of the hosts is down: ",URI
        	break


        #get time
        now = getattr(soup.find('now'), 'string', None)
        starttime = getattr(soup.find('starttime'), 'string', None)
    
        #get hostname
        ccndid = getattr(soup.find('ccndid'), 'string', None)
        host = cfg.hosts.get(ccndid,"Unknown")
    
        # get total CO sent
        co = soup.find('cobs')
        txCO = getattr(co.find('sent'), 'string', None)

        # get total Interests Received
        co = soup.find('interests')
        rxINT = getattr(co.find('accepted'), 'string', None)

        print Decimal(now)-Decimal(starttime), host, txCO, rxINT
        

        #log to server
        #time, host, co, int
        #postVars = {"time":Decimal(now)-Decimal(starttime),"host":hostname,"co":txCO,"int":rxINT}
        #result = urllib.urlopen(cfg.postURI,urllib.urlencode(postVars))
        #print result.read()
        
        #log to server
        data.logDatabase(statusXML, str(Decimal(now)-Decimal(starttime)), host, txCO, rxINT)
