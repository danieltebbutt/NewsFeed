import datetime
import ConfigParser
import boto
from boto.s3.key import Key

config = ConfigParser.ConfigParser()
config.readfp(open('NewsFeed.ini'))

allEntries = []
ENTRY_DATE=0
ENTRY_DESCRIPTION=1
ENTRY_INTEREST=2
ENTRY_SCORE=3

MAX_ENTRIES=5

def calculateScores(allEntries):
    for entry in allEntries:
        entryDate = datetime.datetime.strptime(entry[ENTRY_DATE],"%Y-%m-%d").date()
        entry[ENTRY_DATE]=entryDate
        age = (datetime.date.today() - entryDate).days
        
        # !! Simple score for now, we'll tart it up later
        entry[ENTRY_SCORE] = int(entry[ENTRY_INTEREST]) - age            

def sortEntries(allEntries, key):
    allEntries.sort(key=lambda x: x[key])
    allEntries.reverse()
        
def pickBest(allEntries):
    del allEntries[MAX_ENTRIES:]
        
def prettyDate(date):
    if datetime.date.today().year == date.year:
        # Same year
        pretty = date.strftime("%d %b")
    else:
        # Previous year
        pretty = date.strftime("%d %b %Y")
    return pretty
        
def htmlifyEntries(allEntries):
    html = "<TABLE MARGIN=0>\n"
    for entry in allEntries:
        html += "<TR><TD><B>%s</B></TD><TD>%s</TD></TR>\n"%(prettyDate(entry[ENTRY_DATE]),entry[ENTRY_DESCRIPTION])
    html += "</TABLE>\n"
    return html
        
def upload(content):
    s3 = boto.connect_s3()
    bucket = s3.get_bucket("danieltebbutt.com")
                    
    k = Key(bucket)
    k.key = "newsfeed.html"
    k.set_contents_from_string(content)

def getAllNews():
    source = config.get("NewsFeed", "sourcetype")
    if source == "AWS":
        allEntries = s3GetAllNews()
    elif source == "local":
        allEntries = localGetAllNews()
    return allEntries

def store(allEntries, line):
    split = line.strip().split(",")
    if len(split) == 3:
        split.append(0)
        allEntries.append(split)
    elif len(split) == 4:
        allEntries.append(split)
    elif len(split) != 1:
        print "Duff line '%s' in %s"%(line, file)

def localGetAllNews():
    for file in config.get("NewsFeed", "files").split(","):
        fs = open(file, "r")
        for line in fs:
            store(allEntries, line)
    return allEntries
        
def s3GetAllNews():
    s3 = boto.connect_s3()
    bucketName  = config.get("NewsFeed", "bucket")
    bucket = s3.get_bucket(bucketName)
    k = Key(bucket)

    for file in config.get("NewsFeed", "files").split(","):
        k.key = "newsfeed/%s"%file
        contents = k.get_contents_as_string()
        for line in contents.split("\n"):
            store(allEntries, line)
    return allEntries

allEntries = getAllNews()
calculateScores(allEntries)
sortEntries(allEntries, ENTRY_SCORE)
pickBest(allEntries)
sortEntries(allEntries, ENTRY_DATE)

html = htmlifyEntries(allEntries)
upload(html)
