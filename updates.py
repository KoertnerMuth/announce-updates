import os
import xml.dom.minidom
import time
import datetime


recent_ver = 0
PATH = "Support/RawBin/"
HTMLFILE_DE = "Contents/GLBW.html"
HTMLFILE_EN = "Contents/ELBW.html"
tmpHTMLFILE_DE = "Contents/tmpGLBW.html"
tmpHTMLFILE_EN = "Contents/tmpELBW.html"
RSSFILE_DE = "de.rss"
RSSFILE_EN = "en.rss"


def getVer(path):
    """Liest alle Dateinamen in Support/RawBin/ , um die aktuellste
    Version zu finden.
    """
    recent_ver = 0
    filelist = os.listdir(path)
    for file in filelist:
        if (file.endswith(".txt")):
            fileVer = float(file[:-4])
            if(fileVer > recent_ver):
                recent_ver = fileVer
                print(recent_ver)
                os.rename(PATH + file, PATH + file + ".bak")
                  
    return recent_ver

def updateVer(Ver):
    """Ändere die angezeigte Version in RSS und HTML
    """
    setHTMLVer(Ver, "de")
    setHTMLVer(Ver, "en")
    setRSSVer(Ver, "de")
    setRSSVer(Ver, "en")

def setHTMLVer(Ver, lang):
    """Andert die angezeigte Version in HTML
    """
    verTime = time.gmtime(os.path.getmtime(PATH + str(Ver) + ".txt.bak"))
    formatDatetime = "%i-%i-%i %i:%i" % (verTime.tm_year, verTime.tm_mon, verTime.tm_mday, verTime.tm_hour, verTime.tm_min)
    formatDate = "%i.%i.%i" %(verTime.tm_mday, verTime.tm_mon, verTime.tm_year)
    formatVer = "{0:.3f}".format(Ver)[:-1]
    
    if (lang == "de"):
        srcHTML = HTMLFILE_DE
        headertxt = "Aktuelle LOCKBASE Version: {0}".format(formatVer)
        ptxt = "Die aktuelle LOCKBASE Version {0} steht ab jetzt für Sie zum Update bereit.".format(formatVer)
    elif (lang == "en"):
        srcHTML = HTMLFILE_EN
        headertxt = "Latest LOCKBASE version:  {0}".format(formatVer)
        ptxt = "The latest LOCKBASE version is {0} and can be downloaded ".format(formatVer)

        
    #file = open(os.path.join(os.path.dirname(srcHTML),"tmp" + os.path.basename(srcHTML)), "w")
    dom_file = open(srcHTML, encoding='utf-8')
    dom = xml.dom.minidom.parse(dom_file)
    #RSS root node
    root = dom.documentElement
    articles = root.getElementsByTagName("article")
    for article in articles:
        if (article.hasAttribute("id")):
            article0 = article
            break

    for node in article0.childNodes:
        if node.nodeName == "footer":
            timedate = node.getElementsByTagName("time")[0]
            timedate.setAttribute("datetime", formatDatetime)
            timedate.firstChild.replaceWholeText(formatDate)
        elif node.nodeName == "header":
            header = article0.getElementsByTagName("h1")[0]
            header.firstChild.replaceWholeText(headertxt)
        elif node.nodeName == "p":
            paragraph = article0.getElementsByTagName("p")[0]
            paragraph.firstChild.replaceWholeText(ptxt)

    firstArticle = articles[0]
    firstArticle.parentNode.insertBefore(article0.cloneNode(True), firstArticle)
    firstArticle.parentNode.removeChild(article0)

    file = open(srcHTML, "w")       
    root.writexml(file)
        

def setRSSVer(Ver, lang):
    """Ändert die angezeigte Version in HTML und bewegt das <article>
    Element an oberste Stelle
    """
    ts = time.time()
    pubDateFormat = datetime.datetime.fromtimestamp(ts).strftime('%a, %d %b %Y %H:%M:%S')
    formatVer = "{0:.3f}".format(Ver)[:-1]

    if (lang == "de"):
        srcRSS = RSSFILE_DE
        titletxt = "Aktuelle LOCKBASE Version: {0}".format(formatVer)
        descrtxt = "<p>Die aktuelle LOCKBASE Version {0} steht ab jetzt für Sie zum Update bereit.</p>".format(formatVer)
    elif (lang == "en"):
        srcRSS = RSSFILE_EN
        titletxt = "Latest LOCKBASE Version: {0}".format(formatVer)
        descrtxt = "<p>The latest LOCKBASE Version {0} can be downloaded.</p>".format(formatVer)
    

    dom = xml.dom.minidom.parse(srcRSS)
    #RSS root node
    root = dom.documentElement
    channel = root.childNodes[1]

    for node in channel.childNodes:
        if (node.nodeName == "lastBDate"):
            print("lala")
        elif (node.nodeName == "item"):
            for chNode in node.childNodes:
                if (chNode.nodeName == "title"):
                    chNode.firstChild.replaceWholeText(titletxt)
                elif (chNode.nodeName == "pubDate"):
                    chNode.firstChild.replaceWholeText(pubDateFormat)
                elif (chNode.nodeName == "description"):
                    chNode.firstChild.replaceWholeText(descrtxt)
                break;

    file = open(srcRSS, "w")
    root.writexml(file)

    


recent_ver = getVer(PATH)
#recent_ver = 66.6666
if (recent_ver > 0):
    updateVer(recent_ver)
else:
    print("No update")
