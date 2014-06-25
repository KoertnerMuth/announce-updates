#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import xml.dom.minidom
import time
import datetime
import locale
import email.utils

#Version and features
recent_ver = 0
newFeatures = []

##Strings
#german-strings
ger_htxt = "Aktuelle LOCKBASE Version: {0}"
ger_ptxt = "Die aktuelle LOCKBASE Version {0} steht ab jetzt für Sie zum Update bereit."# <span class=\"more\"><a href=\"Navi.cgi?Topic=GSupport#{0}\">mehr</a></span>"
ger_ftxt = "Neue Features:"

#english-strings
eng_htxt = "Latest LOCKBASE version: {0}"
eng_ptxt = "The latest LOCKBASE version is {0} and can be downloaded"# <a href=\"Navi.cgi?Topic=ESupport#{0}\">here</a>"
eng_ftxt = "New features:"

#Path constants
PATH = "Support/RawBin/"
HTMLFILE_DE = "Contents/GLBW.html"
HTMLFILE_EN = "Contents/ELBW.html"
tmpHTMLFILE_DE = "Contents/tmpGLBW.html"
tmpHTMLFILE_EN = "Contents/tmpELBW.html"
RSSFILE_DE = "de.rss"
RSSFILE_EN = "en.rss"

#URL
supportURL = "http://www.koertner-muth.de/koertner-muth/Navi.cgi?Topic={0}"

#Category
category = "Updates";

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
                if(recent_ver > 0):
                    os.rename(path + str(recent_ver) + ".txt", path + str(recent_ver) + ".txt.bak")
                recent_ver = fileVer
                print(recent_ver)
            #new-Features
            file = open(path + filename)
            lines = file.readlines()
            for i in range(0, len(lines), 3):
                if(lines[i][-4:] == "new\n"): #if 'new' feature
                    newF.append(lines[i+1])#stored in a list, each element is a line
            if(fileVer < recent_ver):
                os.rename(path + str(fileVer) + ".txt", path + str(fileVer) + ".txt.bak")    
              
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
    formatDate = time.strftime('%d.%m.%Y', verTime)

    if (lang == "de_DE.utf8"):
        #formatting german strings
        srcHTML = HTMLFILE_DE
        htxt = ger_htxt.format(formatVer)
        ptxt = ger_ptxt.format(formatVer)
        ftxt = ger_ftxt
    elif (lang == "en_IN"):
        #formatting english strings
        srcHTML = HTMLFILE_EN
        htxt = eng_htxt.format(formatVer)
        ptxt = eng_ptxt.format(formatVer)
        ftxt = eng_ftxt

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
            header.firstChild.replaceWholeText(htxt)
        elif node.nodeName == "p":
            paragraph = article0.getElementsByTagName("p")[0]
            paragraph.firstChild.replaceWholeText(ptxt)
            
            #writing new features to a new paragraph
            if(newFeatures):
                newFElement = dom.createElement("ul") #list containing new feature lines
                li = dom.createElement("li") #list bullet template
                newFElement.setAttribute("class", "newFeatures")
                newFElement.appendChild(dom.createTextNode(ftxt))
                for line in newFeatures:
                    libullet = li.cloneNode(False) 
                    newFElement.appendChild(libullet)
                    libullet.appendChild(dom.createTextNode(line)) #fill bullet with text
                if (paragraph.lastChild.nodeName == "ul" and
                    paragraph.lastChild.hasAttribute("class") and
                    paragraph.lastChild.getAttribute("class") == "newFeatures"): #check if old paragraph exists and needs to be replaced
                            paragraph.replaceChild(newFElement, paragraph.lastChild)
                else:
                    paragraph.appendChild(newFElement)
            else:
                if (paragraph.lastChild.nodeName == "ul" and
                    paragraph.lastChild.hasAttribute("class") and
                    paragraph.lastChild.getAttribute("class") == "newFeatures"): #check if old paragraph exists and needs to be removed
                            paragraph.removeChild(paragraph.lastChild)
                    
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
        titletxt = ger_htxt.format(formatVer)
        descrtxt = "<p>"+ger_ptxt.format(formatVer)+"</p>"
        ftxt = ger_ftxt
        support = "GSupport#{0}".format(formatVer)
    elif (lang == "en"):
        #formatting english strings
        srcRSS = RSSFILE_EN
        titletxt = eng_htxt.format(formatVer)
        descrtxt = "<p>"+eng_ptxt.format(formatVer)+"</p>"
        ftxt = eng_ftxt
        support = "ESupport#{0}".format(formatVer)

    #adding new-features list to description text
    if (newFeatures):
        descrtxt += "<ul class = \"newFeatures\">" + ftxt
        for line in newFeatures:
            descrtxt += "<li>" + line + "</li>"
        descrtxt += "</ul>"
    
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
                node.getElementsByTagName("link")[0].firstChild.replaceWholeText(supportURL.format(support))
                node.getElementsByTagName("pubDate")[0].firstChild.replaceWholeText(pubDateFormat)
                node.getElementsByTagName("category")[0].firstChild.replaceWholeText(category)
                node.getElementsByTagName("guid")[0].firstChild.replaceWholeText(supportURL.format(support))
                descrElement = node.getElementsByTagName("description")[0]
                descrElement.firstChild.replaceWholeText(descrtxt)

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
#recent_ver = 11.11
if (recent_ver > 0):
    updateVer(recent_ver)
    os.rename(PATH + str(recent_ver) + ".txt", PATH + str(recent_ver) + ".txt.bak")
else:
    print("No update")
