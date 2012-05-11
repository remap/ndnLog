import re
import sys
import pymongo
from pymongo import Connection
from pymongo.errors import CollectionInvalid
import datetime
import time
from pymongo import ASCENDING, DESCENDING
from pymongo.code import Code
import string
import json
from decimal import *

import config as cfg
#87

connection = Connection('localhost', cfg.dbPort)
#db = connection.test
#collection = db.test

db = connection[cfg.colName]
collection = db[cfg.colName]

def index(req):
  	sys.stderr = sys.stdout
  	req.content_type = "text/plain"
  	req.write("Hello World!\n")
  	anotherMethod(req)
  	#writeDatabase(req)
  	
def anotherMethod(req):
	req.write("another method...\n")
	
def writeDatabase(name, email, title, comment):
    #connect to mongoDB
	#connection = Connection()
	#db = connection.test
	#collection = db.test
	
	data = post={"author":name, "title":title, "text":comment, "email":email, "tags":["UCLA","TFT","festival", "test"],"date":datetime.datetime.utcnow()}
	
	lastID = collection.insert(data)
	
	return lastID
	
def logDatabase(statusXML, runtime, ccndid, host, co, int):
    #connect to mongoDB
	#connection = Connection()
	#db = connection.test
	#collection = db.test
	
	data = post={"statusXML":statusXML, "time":time.time(), "ccndid":ccndid, "host":host, "coRX":co, "intTX":int}
	
	lastID = collection.insert(data)
	
	return lastID

def clearDatabase():
	# clear collection
	db.drop_collection(cfg.colName)

def getEntryFromID(id):
	return(collection.find_one({"_id":id}))


def updateFilenameFromID(id,filename):
	
	collection.update({"_id":id }, { "$push": { "filename":filename} } );
	
	return getEntryFromID(id)
	
	
def insertAnalysisWithID(id,aName,analysisResult):
	
	collection.update({"_id":id }, { "$push": { "analysis":{"analysisName":aName, "result":analysisResult}}} );
	
	return getEntryFromID(id)
	

def getFilenameFrom(id):
	entry = getEntryFromID(id)	
	return str(entry['filename'][0])

###### unused methods follow
	
def getAllUnanalyzed():
	# get all entries that have no 'analysis' field
	
	#return(collection.find( { analysis : { $exists : false } } ));
	# or something like that 
	
	return


def getAllAnalyzed():
	#get all entries that have been analyzed
	return collection.find( { "analysis" : { "$exists" : "true"} } );

	
def getLastEntry():

	
	lastEntry = collection.find_one(sort = [('_id',DESCENDING)])
	
	return lastEntry
	

def getLastForEachHost(req):

	hostData = []
	for host in cfg.hosts:
		#print cfg.hosts[host]
		lastEntry = collection.find_one({'host':cfg.hosts[host]}, sort = [('_id',DESCENDING)])
		item = [lastEntry['host'],lastEntry['time'],lastEntry['coRX'],lastEntry['intTX']]
		hostData.append(item)
		#print lastEntry['host'],lastEntry['time'],lastEntry['coRX'], lastEntry['intTX']
		#jsonResult = '( "host": "'+lastEntry['host']+'", "time": "'+lastEntry['time']+'", "co": "'+lastEntry['coRX']+'", "int": "'+lastEntry['intTX']+'")'
		#hostData = hostData + "," + jsonResult
		# don't manually build json! use internal libs...
	#hostData = string.lstrip(hostData,",")	
	return 'data = '+json.dumps(hostData)

def getCOForAreaChart(req):

	labels = []
	values = []
	out = ""
	depth = 3
	startVals = {'label':'start','values':[]}
	for host in cfg.hosts:
		# get all entries for host
		fEnt = collection.find_one({'host':cfg.hosts[host]}, sort = [('_id',ASCENDING)])
		lastEntries = collection.find({'host':cfg.hosts[host]}, sort = [('_id',DESCENDING)]).limit(depth)
		# populate host
		labels.append(fEnt['host'])
		# populate values
		startVals['values'].append(fEnt['coRX'])
		idx = 0
		for ent in lastEntries:
			if len(startVals['values']) == 1: # if this is first pass of values list
				value = {'label':'','values':[]}
				value['label'] =  ent['time']
				value['values'] = []
				value['values'].append(ent['coRX'])
				values.append(value)
			else: #second pass, thus take care to append:
				values[idx]['values'].append(ent['coRX'])
				idx = idx + 1
				
	totalData = {'label':'','values':[]}
	totalData['label'] = labels
	values.append(startVals)
	totalData['values'] = values
		
	return 'json = '+json.dumps(totalData, sort_keys=True, indent=4)
		
def getCOForAreaChartDebug(req):

	labels = []
	values = []
	out = ""
	depth = cfg.plotDepth
	# 3 hosts:
	# 20000 was ok (slow, but worked) with 3 hosts
	# 2000 and it starts to slow down
	# 1000 is still smooth
	# 200 will be fast
	
	# no depth; plot everything
	first = collection.find(sort = [('_id',ASCENDING)]).limit(len(cfg.hosts))
	events = collection.find({},sort = [('_id',ASCENDING)]).limit(depth*len(cfg.hosts))
	val = []
	for e in events:
		# we only want the *change* - 
		val.append(float(e['coRX'])-float(first[len(val)]['coRX']))
		if (len(val)==len(cfg.hosts)):
			counter=len(values)+1
			values.append({'label':str(counter),'values':val})
			val = []
	totalData = {'label':cfg.hosts.values(),'values':values}
		#out += e['host']+" : "
		#out += e['time']+" \n"
	return 'json = '+json.dumps(totalData, sort_keys=True, indent=4)


def buildHosts(rec):
	ccndidict = {}
	for r in rec:
		if r['ccndid'] not in ccndidict:
			ccndidict.update({r['ccndid']:r['host']})
	return ccndidict;
	

def getCOForAreaChartDynamicHosts(req):
	labels = []
	values = []
	out = ""
	depth = 150
	skipVal = 0
	# 3 hosts:
	# 20000 was ok (slow, but worked) with 3 hosts
	# 2000 and it starts to slow down
	# 1000 is still smooth
	# 200 will be fast

	# get all records
	allEvents = collection.find({},sort = [('time',ASCENDING)])
	
	# get unique hosts from query
	hosts = buildHosts(allEvents);
	
	# make 'framebuffer'
	fb = hosts.copy()
	for key in fb:
		fb[key] = 0.0;
	# make 'initial values'
	iv = fb.copy()

	#if((allEvents.count()-depth*len(hosts))>0):
	#	skipVal = allEvents.count()-depth*len(hosts)

	# get subset to plot
	events = collection.find({},sort = [('time',ASCENDING)]).limit(depth*len(hosts)).skip(skipVal)
	for e in events:
		if(iv[e['ccndid']] == 0):
			iv[e['ccndid']] = e['coRX']
		fb[e['ccndid']]=(float(e['coRX']) - float(iv[e['ccndid']]))
		counter=len(values)+1
		#make framebuffer
		values.append({'label':str(counter),'values':fb.values()})
	
	totalData = {'label':hosts.values(),'values':values, 'debug':iv}
	

	return 'json = '+json.dumps(totalData, sort_keys=True, indent=4)


def getFirstEvent():
	return True


def getCOForAreaChartDebug2(req):

	labels = []
	values = []
	out = ""
	startVals = {'label':'start','values':[]}
	for host in cfg.hosts:
		# get all entries for host
		fEnt = collection.find_one({'host':cfg.hosts[host]}, sort = [('_id',ASCENDING)])
		lastEntries = collection.find({'host':cfg.hosts[host]}, sort = [('_id',DESCENDING)]).limit(3)
		# populate host
		labels.append(fEnt['host'])
		# populate values
		startVals['values'].append(fEnt['coRX'])
		idx = 0
		for ent in lastEntries:
			out += fEnt['host']+" : "
			out += ent['time']+" \n"
				
	return out
	
'''
#MAP REDUCE - sorta working ish 

map = Code("function() {for (var key in this) { emit(key, null); }}")
reduce = Code("function(key, stuff) { return null; }")

result = collection.map_reduce(map,reduce,"host").distinct("_id")

for doc in result:
	out+=doc+"\n"
'''
