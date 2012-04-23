import re
import sys
import pymongo
from pymongo import Connection
from pymongo.errors import CollectionInvalid
import datetime
import time
from pymongo import ASCENDING, DESCENDING
import string
import json

import config as cfg

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
	
def logDatabase(statusXML, runtime, host, co, int):
    #connect to mongoDB
	#connection = Connection()
	#db = connection.test
	#collection = db.test
	
	data = post={"statusXML":statusXML, "time":runtime, "host":host, "coRX":co, "intTX":int}
	
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
		