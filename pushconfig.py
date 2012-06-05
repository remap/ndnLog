# mongodb collection name
#colName = "ndnvideoEC2"
colName = "ndnvideoEC2_0" #_5 is naked ccnid for host

# mongod port
dbPort = 27017 #27017 is default

#delay per URI status loop
loopDelay =2

#if posting via HTTP instead of writing direct to mongodb
postURI = "http://borges.metwi.ucla.edu/ec2/ndnLog/database.py/logDatabase"

#URIs of status XML to scrape
URIs = ["http://localhost:9695/?f=xml"]


#CCNDID to Hostname mapping - to augment dynamic 
# currently pulling... when pushing, insert hostname
hosts = {"BD69492C535993B1A27D56E3E1258F3B982F3E07E75B187191350A3A14ABAF57":"BORGES",
         "CD940B127506EECBD2298CCFDC3BC41C179611D43DB43363F00DF70EA7245AC2":"HYDRA",
         "FCC3C775E6653244A5DCB870BE4A80FBC417A39B0A3286B7548C1F6BAA8C8B5A":"PARC",
         "156681532B9D55AAFF175D91CC5058311F6E1F06C4760EA381E1AFC457000E21":"UCLA-DEV",
         "24D91482469C51E7A74285A31E9C53AF26D151443C0B2057C879D980FC573BDB":"UIUC"}