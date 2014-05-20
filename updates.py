import os

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
    setHTMLVer(Ver, "en")
    #setRSSVer(Ver, "de")
    #setRSSVer(Ver, "en")

def setHTMLVer(Ver, lang):
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
							  Aktuelle LOCKBASE Version: %f
							</h1>
						</header>
						<p>
						  Die aktuelle LOCKBASE Version %f steht ab jetzt für Sie zum Update bereit. 
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
								Latest LOCKBASE version:  %f
							</h1>
						</header>
						<p>
							The latest LOCKBASE version is %f and can be downloaded  			
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
        
        

#def setRSSVer(Ver, lang):
#    """Ändert die angezeigte Version in HTML und bewegt das <article>
#    Element an oberste Stelle
#    """
    


current_ver = getVer(PATH)
updateVer(current_ver)
