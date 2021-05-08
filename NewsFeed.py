import .NewsBackend
import ConfigParser
import boto
from boto.s3.key import Key

allEntries = []

config = ConfigParser.ConfigParser()
config.readfp(open('NewsFeed.ini'))

def upload(content, target = NEWSFEED):
    s3 = boto.connect_s3(is_secure = False)
    bucket = s3.get_bucket(BUCKET, validate = False)
                    
    k = Key(bucket)
    k.key = target
    k.set_contents_from_string(content)
    
def getAllNews():
    source = config.get("NewsFeed", "sourcetype")
    if source == "AWS":
        allEntries = s3GetAllNews()
    elif source == "local":
        allEntries = localGetAllNews()
    return allEntries

def localGetAllNews():
    for file in config.get("NewsFeed", "files").split(","):
        fs = open(file, "r")
        for line in fs:
            store(allEntries, line)
    return allEntries
        
def s3GetAllNews():
    s3 = boto.connect_s3(is_secure=False)
    bucketName  = config.get("NewsFeed", "bucket")
    bucket = s3.get_bucket(bucketName, validate = False)
    k = Key(bucket)

    for file in config.get("NewsFeed", "files").split(","):
        k.key = "newsfeed/%s"%file
        contents = k.get_contents_as_string()
        for line in contents.split("\n"):
            store(allEntries, line)
    return allEntries

if __name__ == "__main__":
    allEntries = getAllNews()
    calculateScores(allEntries)
    sortEntries(allEntries, ENTRY_SCORE)
    html = debugHtml(allEntries)
    upload(html, "debugnews.html")
    pickBest(allEntries)
    sortEntries(allEntries, ENTRY_DATE)

    html = htmlifyEntries(allEntries)
    upload(html)
