import datetime

ENTRY_TYPE=0
ENTRY_DATE=1
ENTRY_DESCRIPTION=2
ENTRY_INTEREST=3
ENTRY_SCORE=4

MAX_ENTRIES=20

NEWSFEED="newsfeed.html"
BUCKET="danieltebbutt.com"

def calculateScores(allEntries):
    for entry in allEntries:
        entryDate = datetime.datetime.strptime(entry[ENTRY_DATE],"%Y-%m-%d").date()
        entry[ENTRY_DATE]=entryDate
        age = (datetime.date.today() - entryDate).days
       
        # Start with the interest value
        entry[ENTRY_SCORE] = int(entry[ENTRY_INTEREST])

        # Subtract age in weeks
        entry[ENTRY_SCORE] -= (age/7)
 
        # Special boost for recent news
        if entry[ENTRY_TYPE] == "NEWS":
            if age <= 7:
                entry[ENTRY_SCORE] += 20
            elif age <= 31:
                entry[ENTRY_SCORE] += 10
          
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
        
def image(type):
    if type == "RUN":
        return "<IMG SRC=\"icons/run.png\" width=20 height=20></IMG>"
    elif type == "NEWS":
        return "<IMG SRC=\"icons/news.png\" width=20 height=20></IMG>"
    elif type == "RACE":
        return "<IMG SRC=\"icons/medal.png\" width=20 height=20></IMG>"
    elif type == "RUNTOTAL":
        return "<IMG SRC=\"icons/road.png\" width=20 height=20></IMG>"
    else:
        return ""
        
def htmlifyEntries(allEntries):
    html = "<TABLE MARGIN=0>\n"
    for entry in allEntries:
        html += "<TR><TD>%s</TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n"%(image(entry[ENTRY_TYPE]), prettyDate(entry[ENTRY_DATE]), entry[ENTRY_DESCRIPTION])
    html += "</TABLE>\n"
    return html
        
def debugHtml(allEntries):
    html = "<TABLE MARGIN=0>\n"
    html += "<TR><TD>Index</TD><TD>Type</TD><TD>Date</TD><TD>Score</TD><TD>Interest</TD><TD>Description</TD></TR>\n"
    ii=1  
    for entry in allEntries:
        html += "<TR><TD>%d</TD><TD>%s</TD><TD>%s</TD><TD>%d</TD><TD>%s</TD><TD>%s</TD></TR>\n"%(ii,
                                                                                                 entry[ENTRY_TYPE], 
                                                                                                 entry[ENTRY_DATE], 
                                                                                                 entry[ENTRY_SCORE], 
                                                                                                 entry[ENTRY_INTEREST], 
                                                                                                 entry[ENTRY_DESCRIPTION])
        ii += 1
    html += "</TABLE>\n"
    return html

def store(allEntries, line):
    split = line.strip().split(",")
    if len(split) == 4:
        split.append(0)
        allEntries.append(split)
    elif len(split) == 5:
        allEntries.append(split)
    elif len(split) != 1:
        print("Duff line '%s' in %s"%(line, file))

