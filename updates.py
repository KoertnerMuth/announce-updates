#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import xml.dom.minidom
import time
import datetime
import locale
import email.utils

#Path constants
PATH = "Support/RawBin/"
HTMLFILE_DE = "Contents/GLBW.html"
HTMLFILE_EN = "Contents/ELBW.html"
tmpHTMLFILE_DE = "Contents/tmpGLBW.html"
tmpHTMLFILE_EN = "Contents/tmpELBW.html"
RSSFILE_DE = "de.rss"
RSSFILE_EN = "en.rss"

#Version and features
recent_ver = 0
newFeatures = []

def getVer(path):
    """Liest alle Dateinamen in Support/RawBin/ , um die aktuellste
    Version zu finden.
    """
    newF = []
    recent_ver = 0
    filelist = os.listdir(path)
    for filename in filelist:
        if (filename.endswith(".txt")):
            #getting latest version number
            fileVer = float(filename[:-4])
            if(fileVer > recent_ver):
                recent_ver = fileVer
                print(recent_ver)
            #new-Features
            file = open(PATH + filename)
            lines = file.readlines()
            for i in range(0, len(lines), 3):
                if(lines[i][-4:] == "new\n"):#if 'new' feature
                    newF.append(lines[i+1])#stored in a list, each element is a line
              
    return [recent_ver, newF] #returned in a pair

def updateVer(Ver):
    """Ändere die angezeigte Version in RSS und HTML
    """
    setHTMLVer(Ver, "de_DE.utf8")
    setHTMLVer(Ver, "en_IN")
    setRSSVer(Ver, "de")
    setRSSVer(Ver, "en")

def setHTMLVer(Ver, lang):
    """Andert die angezeigte Version in HTML
    """
    #formatting multi-lang strings
    locale.setlocale(locale.LC_ALL, lang) #for dateformatting
    verTime = time.gmtime(os.path.getmtime(PATH + str(Ver) + ".txt")) #time of latest version .txt
    
    formatVer = "{0:.3f}".format(Ver)[:-1] #for truncating to having 2 decimal points
    formatDatetime = time.strftime('%Y-%m-%d %H:%M:%S%z', verTime)
    formatDate = time.strftime('%x', verTime)

    if (lang == "de_DE.utf8"):
        #formatting german strings
        srcHTML = HTMLFILE_DE
        headertxt = "Aktuelle LOCKBASE Version: {0}".format(formatVer)
        ptxt = "Die aktuelle LOCKBASE Version {0} steht ab jetzt für Sie zum Update bereit.".format(formatVer)
        ftxt = "Neue Features:"
    elif (lang == "en_IN"):
        #formatting english strings
        srcHTML = HTMLFILE_EN
        headertxt = "Latest LOCKBASE version: {0}".format(formatVer)
        ptxt = "The latest LOCKBASE version is {0} and can be downloaded ".format(formatVer)
        ftxt = "New features:"

    #DOM manipulation
    dom_file = open(srcHTML, encoding='utf-8')
    dom = xml.dom.minidom.parse(dom_file)
    
    root = dom.documentElement #HTML root node
    articles = root.getElementsByTagName("article")
    #finding version-articlenode
    for article in articles:
        if (article.hasAttribute("id")):
            if (article.getAttribute("id") == "version"):
                article0 = article #found version-article
            break

    #editting strings of version-article
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
            #writing new features to a new paragraph
            brElement = dom.createElement("br") #linebreak element
            newFElement = dom.createElement("p") #paragraph containing new feature lines
            newFElement.setAttribute("id", "newFeatures")
            newFElement.appendChild(dom.createTextNode(ftxt))
            for line in newFeatures:
                newFElement.appendChild(brElement.cloneNode(False))
                newFElement.appendChild(dom.createTextNode(" - " + line))
            if (paragraph.lastChild.hasAttribute("id")):
                if (paragraph.lastChild.getAttribute("id") == "newFeatures"):
                    paragraph.replaceChild(newFElement, paragraph.lastChild)
            else:
                paragraph.appendChild(newFElement)
                    
    #moving edited article at the top
    firstArticle = articles[0]
    firstArticle.parentNode.insertBefore(article0.cloneNode(True), firstArticle)
    firstArticle.parentNode.removeChild(article0)

    #saving file
    file = open(srcHTML, "w")       
    root.writexml(file)
        

def setRSSVer(Ver, lang):
    """Ändert die angezeigte Version in HTML und bewegt das <article>
    Element an oberste Stelle
    """
    #formatting multi-lang strings
    verTime = time.gmtime(os.path.getmtime(PATH + str(Ver) + ".txt"))
    pubDateFormat = time.strftime("%a, %d %b %Y %H:%M:%S %z", verTime)
    buildDateFormat = email.utils.formatdate(localtime=True)
    formatVer = "{0:.3f}".format(Ver)[:-1]

    if (lang == "de"):
        #formatting german strings
        srcRSS = RSSFILE_DE
        titletxt = "Aktuelle LOCKBASE Version: {0}".format(formatVer)
        descrtxt = "<p>Die aktuelle LOCKBASE Version {0} steht ab jetzt für Sie zum Update bereit.</p>".format(formatVer)
        ftxt = "Neue Features:"
    elif (lang == "en"):
        #formatting english strings
        srcRSS = RSSFILE_EN
        titletxt = "Latest LOCKBASE Version: {0}".format(formatVer)
        descrtxt = "<p>The latest LOCKBASE Version {0} can be downloaded.</p>".format(formatVer)
        ftxt = "New features:"
    
    #DOM manipulation
    dom = xml.dom.minidom.parse(srcRSS)
    #RSS root node
    root = dom.documentElement
    channel = root.childNodes[1]
    
    for node in channel.childNodes:
        if (node.nodeName == "lastBuildDate"):
            node.firstChild.replaceWholeText(buildDateFormat)
        elif (node.nodeName == "item"):
            #checking if item is version-item
            if(node.getElementsByTagName("title")[0].firstChild.nodeValue[:-6] == titletxt[:-6]):
                versionNode = node
                node.getElementsByTagName("title")[0].firstChild.replaceWholeText(titletxt)
                node.getElementsByTagName("pubDate")[0].firstChild.replaceWholeText(pubDateFormat)
                descrElement = node.getElementsByTagName("description")[0]
                descrElement.firstChild.replaceWholeText(descrtxt)
                
                #adding new feature element
                newFElement = dom.createElement("newfeat") #element containing new feature lines
                newFElement.appendChild(dom.createTextNode(ftxt))
                for line in newFeatures:
                    newFElement.appendChild(dom.createTextNode(" - " + line))
                print(descrElement.lastChild.nodeName)
                if (descrElement.lastChild.nodeName == "newfeat"): #old new feature element found
                    print("replace")
                    descrElement.replaceChild(newFElement, descrElement.lastChild)
                else:
                    print("append")
                    descrElement.appendChild(newFElement)
                break;

    #moving edited version-item at the top
    firstItem = channel.getElementsByTagName("item")[0]
    firstItem.parentNode.insertBefore(versionNode.cloneNode(True), firstItem)
    firstItem.parentNode.removeChild(versionNode)

    #saving file
    file = open(srcRSS, "w")
    root.writexml(file)

    

ver_feat = getVer(PATH)
recent_ver = ver_feat[0]
newFeatures = ver_feat[1]
recent_ver = 11.11
if (recent_ver > 0):
    updateVer(recent_ver)
    #os.rename(PATH + filename, PATH + filename + ".bak")
else:
    print("No update")
