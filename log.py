import sys
#sys.path.append("/var/www/html/lighting/app")

import os
#os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import config as cfg

import database as data


# if not auth
	# return apache.HTTP_FORBIDDEN

# accept image upload

	# save temp image

	# make new media record
	
	#rename & save image, UID suffix


def postData(req, time, host, co, int):
	#req.write("posting data: "+time+" : "+host+" : "+co+" : "+int+" \n")
	lastID = data.logDatabase(time, host, co, int)
	#req.write("OK "+ str(lastID))
	return "OK : ",lastID