# mongodb collection name
#colName = "ndnvideoEC2"
colName = "ndnvideoEC2_0"

# mongod port
dbPort = 27017 #27017 is default

#delay per URI status loop
loopDelay =2

#if posting via HTTP instead of writing direct to mongodb
postURI = "http://borges.metwi.ucla.edu/ec2/ndnLog/log.py/postData"

#URIs of status XML to scrape
URIs = ["http://hydra.remap.ucla.edu:9695/?f=xml",
        "http://borges.metwi.ucla.edu:9695/?f=xml"]
       # "http://ccngw.parc.xerox.com:9695/?f=xml",
        #"http://ndn.cs.illinois.edu:9695/?f=xml"]


#CCNDID to Hostname mapping - to augment dynamic 
# currently pulling... when pushing, insert hostname
hosts = {"BD69492C535993B1A27D56E3E1258F3B982F3E07E75B187191350A3A14ABAF57":"BORGES",
         "CD940B127506EECBD2298CCFDC3BC41C179611D43DB43363F00DF70EA7245AC2":"HYDRA"}