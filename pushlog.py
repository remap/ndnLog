import xml
import json
import urllib
from BeautifulSoup import BeautifulSoup
import pushconfig as cfg
import time
from decimal import *
import platform

sysStartTime = time.time()

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

        #get ccnd time
        now = getattr(soup.find('now'), 'string', None)
        starttime = getattr(soup.find('starttime'), 'string', None)

        #get hostname
        ccndid = getattr(soup.find('ccndid'), 'string', None)
        hostname = platform.node()

        # get total CO sent
        co = soup.find('cobs')
        txCO = getattr(co.find('sent'), 'string', None)

        # get total Interests Received
        co = soup.find('interests')
        rxINT = getattr(co.find('accepted'), 'string', None)

        #per-host time is not needed right now...
        #let's replace w/ experiment time
        expTime = time.time()-sysStartTime

        print expTime, hostname, txCO, rxINT, ccndid

        #print urllib.urlencode({"statusXML":statusXML, "time":time.time(), "ccndid":ccndid, "host":hostname, "coRX":txCO, "intTX":rxINT})
        params = urllib.urlencode({"statusXML":statusXML, "runtime":time.time(), "ccndid":ccndid, "host":hostname, "co":txCO, "int":rxINT})
		
		#statusXML, runtime, ccndid, host, co, int
		
		# doesn't matter what time is, it will be over-written on insertion
		#

        f = urllib.urlopen(cfg.postURI, params)

#postVars = urllib.urlencode({"statusXML":statusXML,"time":time.time(),"ccndid":ccndid,"host":hostname,"txCO":txCO,"rxINT":rxINT})

        print f.read()

            #result = urllib.urlopen(cfg.postURI,urllib.urlencode(postVars))
        #print result.read()
