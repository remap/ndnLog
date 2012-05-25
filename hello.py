from mod_python import apache
import sys
 
def index(req):
  	sys.stderr = sys.stdout
  	req.content_type = "text/plain"
  	req.write("Hello World!\n")
  	#anotherMethod(req)
  	#writeDatabase(req)
  	