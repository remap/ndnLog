import os
import commands
import ConfigParser
import io
import urllib
import time

# config

config = ConfigParser.RawConfigParser()
configFile = os.path.dirname(__file__)+'/logger.cfg'
config.readfp(open(configFile))

# Logger

def logStart():
	fullCLI = "ssh ec2@borges.metwi.ucla.edu /home/ec2/system/startLog"
	result = commands.getoutput(fullCLI)
	return result
	
def logStop():
	fullCLI = "ssh ec2@borges.metwi.ucla.edu /home/ec2/system/stopLog"
	result = commands.getoutput(fullCLI)
	return result

def logReset():
	# increment collection name so we can save the experiments
	config.readfp(open(configFile))
	num = int(config.get("mongo", "lognumber"))
	num = num + 1
	config.set('mongo', 'lognumber', str(num))
	with open(configFile, 'wb') as file:
		config.write(file)
	#time.sleep(1)
	# reset database collection to new collection
	resetURI = "http://borges.metwi.ucla.edu/ec2/ndnLog/database.py/resetConnection"
	status = urllib.urlopen(resetURI)
	#return "log clear, now on "+str(num)
	return "plot clear, "+status.read()

# EC2

# start N ec2 instances
def ec2Start(howmany):
	#return "starting "+howmany+" ec2 instances in "+config.get("ec2", "region")
	fullCLI = "ssh ec2@borges.metwi.ucla.edu /home/ec2/system/startInstances "+howmany
	result = commands.getoutput(fullCLI)
	return result
	
def ec2Stop():
	#return "killing all ec2 instances"
	fullCLI = "ssh ec2@borges.metwi.ucla.edu /home/ec2/system/stopInstances"
	result = commands.getoutput(fullCLI)
	return result




#def start(howMany):
	#fullCLI = "ssh "+cfg.host+" "+cfg.path" command"
	#fullCLI = "ssh ec2@borges.metwi.ucla.edu /home/ec2/system/"
	#result = commands.getoutput(fullCLI)
	#return "result : " +result


# stop all ec2 instances

