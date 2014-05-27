import os
import xml.dom.minidom
import time
import datetime

#Aktuelle Version init auf 0
current_ver = 0
PATH = "Support/RawBin/"
HTMLFILE_DE = "Contents/GLBW.html"
HTMLFILE_EN = "Contents/ELBW.html"
tmpHTMLFILE_DE = "Contents/tmpGLBW.html"
tmpHTMLFILE_EN = "Contents/tmpELBW.html"
RSSFILE_DE = "de.rss"
RSSFILE_EN = "en.rss"

debug = True

def getVer(path):
    """Liest alle Dateinamen in Support/RawBin/ , um die aktuellste
    Version zu finden.
    """
    recentVer = 0
    filelist = os.listdir(path)
    for file in filelist:
        if (file.endswith(".txt")):
            fileVer = float(file[:-4])
            if(fileVer > recentVer):
                recentVer = fileVer
                print(recentVer)
                os.rename(PATH + file, PATH + file + ".bak")
                  
    return recentVer

def updateVer(Ver):
    """Ändere die angezeigte Version in RSS und HTML
    """
    setHTMLVer(Ver, "de")
    #setHTMLVer(Ver, "en")
    #setRSSVer(Ver, "de")
    #setRSSVer(Ver, "en")

def setHTMLVer(Ver, lang):
    """Andert die angezeigte Version in HTML
    """
    if (lang == "de"):
        file_de = open(tmpHTMLFILE_DE, "w")
        dom_file = open(HTMLFILE_DE, encoding='utf-8')
        dom = xml.dom.minidom.parse(dom_file)
        #RSS root node
        #root = dom.documentElement
        #section1 = root.getElementsByTagName("section")
        
            
##        lastBDate = channel.getElementsByTagName("lastBuildDate")[0]
##        verItem = channel.getElementsByTagName("item")[0]
##        title = verItem.getElementsByTagName("title")[0].firstChild
##        title.replaceWholeText("Aktuelle LOCKBASE Version: %f" % (Ver,))
##        pubDate = verItem.getElementsByTagName("pubDate")[0].firstChild
##        pubDate.replaceWholeText(pubDateFormat)
##        descr = verItem.getElementsByTagName("description")[0].firstChild
##        descr.replaceWholeText("<p>Die aktuelle LOCKBASE Version %f steht ab jetzt für Sie zum Update bereit.</p>" % (Ver,))
##        print(descr)
##        print(descr.nodeValue)
##        print(verItem)
##        root.writexml(file_de)

def old_setHTMLVer(Ver, lang):
    """Ändert die angezeigte Version in HTML
    """
    verTime = time.gmtime(os.path.getmtime(PATH + str(Ver) + ".txt.bak"))
    formatDatetime = "%i-%i-%i %i:%i" % (verTime.tm_year, verTime.tm_mon, verTime.tm_mday, verTime.tm_hour, verTime.tm_min)
    formatDate = "%i.%i.%i" %(verTime.tm_mday, verTime.tm_mon, verTime.tm_year)

    if (lang == "de"):
        infile = open(HTMLFILE_DE, 'r')
        outfile = open(tmpHTMLFILE_DE, 'w')
        tmpLine = infile.readline()
        while ("<article id=\"version\">" not in tmpLine):
            outfile.write(tmpLine)
            tmpLine = infile.readline()
        outfile.write("""<article id="version">
						<footer>
						  <time datetime="%s">
						    %s
						  </time>
						</footer>
						<header>
							<h1>
							  Aktuelle LOCKBASE Version: %0.2f
							</h1>
						</header>
						<p>
						  Die aktuelle LOCKBASE Version %0.2f steht ab jetzt für Sie zum Update bereit. 
						    <span class="more">
						      <a href="@NAVI=GSupport">
							mehr
						      </a>
						    </span>
						</p>
					</article>""" % (formatDatetime, formatDate, Ver, Ver))
                      
        while ("</article>" not in tmpLine):
                      tmpLine = infile.readline()
                      
        for line in infile:
            outfile.write(line)
        infile.close()
        outfile.close()
        #os.rename(tmpHTMLFILE_DE, HTMLFILE_DE)
    elif (lang == "en"):
        infile = open(HTMLFILE_EN, 'r')
        outfile = open(tmpHTMLFILE_EN, 'w')
        tmpLine = infile.readline()
        while ("<article id=\"version\">" not in tmpLine):
            outfile.write(tmpLine)
            tmpLine = infile.readline()
        outfile.write("""<article id="version">
						<footer>
							<time datetime="%s">
								%s
							</time>
						</footer>
						<header>
							<h1>
								Latest LOCKBASE version:  %0.2f
							</h1>
						</header>
						<p>
							The latest LOCKBASE version is %0.2f and can be downloaded  			
							<span class="more">
							<a href="@NAVI=GSupport">
								here
							</a>
						</span>
						</p>
					</article>""" % (formatDatetime, formatDate, Ver, Ver))
                      
        while ("</article>" not in tmpLine):
                      tmpLine = infile.readline()
                      
        for line in infile:
            outfile.write(line)
        infile.close()
        outfile.close()
        #os.rename(tmpHTMLFILE_EN, HTMLFILE_EN)
        
        

def setRSSVer(Ver, lang):
    """Ändert die angezeigte Version in HTML und bewegt das <article>
    Element an oberste Stelle
    """
    ts = time.time()
    pubDateFormat = datetime.datetime.fromtimestamp(ts).strftime('%a, %d %b %Y %H:%M:%S')

    if (lang == "de"):
        #TODO: Edit file_de to path RSSFILE_DE (without tmp)
        file_de = open("tmp" + RSSFILE_DE, "w")
        dom = xml.dom.minidom.parse(RSSFILE_DE)
        #RSS root node
        root = dom.documentElement
        channel = root.childNodes[1]
        lastBDate = channel.getElementsByTagName("lastBuildDate")[0]
        verItem = channel.getElementsByTagName("item")[0]
        title = verItem.getElementsByTagName("title")[0].firstChild
        title.replaceWholeText("Aktuelle LOCKBASE Version: %0.2f" % (Ver,))
        pubDate = verItem.getElementsByTagName("pubDate")[0].firstChild
        pubDate.replaceWholeText(pubDateFormat)
        descr = verItem.getElementsByTagName("description")[0].firstChild
        descr.replaceWholeText("<p>Die aktuelle LOCKBASE Version %0.2f steht ab jetzt für Sie zum Update bereit.</p>" % (Ver,))
        print(descr)
        print(descr.nodeValue)
        print(verItem)
        root.writexml(file_de)

    elif (lang == "en"):
        #TODO: Edit file_de to path RSSFILE_EN (without tmp)
        file_de = open("tmp" + RSSFILE_EN, "w")
        dom = xml.dom.minidom.parse(RSSFILE_EN)
        #RSS root node
        root = dom.documentElement
        channel = root.childNodes[1]
        lastBDate = channel.getElementsByTagName("lastBuildDate")[0]
        verItem = channel.getElementsByTagName("item")[0]
        title = verItem.getElementsByTagName("title")[0].firstChild
        title.replaceWholeText("Latest LOCKBASE Version: %0.2f" % (Ver,))
        pubDate = verItem.getElementsByTagName("pubDate")[0].firstChild
        pubDate.replaceWholeText(pubDateFormat)
        descr = verItem.getElementsByTagName("description")[0].firstChild
        descr.replaceWholeText("<p>The latest LOCKBASE Version %0.2f can be downloaded.</p>" % (Ver,))
        print(descr)
        print(descr.nodeValue)
        print(verItem)
        root.writexml(file_de)
    


#current_ver = getVer(PATH)
current_ver = 66.666
updateVer(current_ver)
