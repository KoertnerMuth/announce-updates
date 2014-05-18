import os

#Aktuelle Version init auf 0
current_ver = 0

def readVer():
    """Liest alle Dateinamen in Support/RawBin/ , um die aktuellste Version
    zu finden.
    """
    recentVer    
    filelist = os.listdir('/Support/RawBin/')
    for file in filelist:
        #vergleiche file-name mit current_ver
    return recentVer

def updateVer(Ver):
    """Ändere die angezeigte Version in RSS und HTML
    """
    setHTMLVer(Ver)
    setRSSVer(Ver)

def setHTMLVer(Ver):
    """Ändert die angezeigte Version in HTML und bewegt das <article> Element
    an oberste Stelle
    """

def setRSSVer(Ver)
    """Ändert die angezeigte Version in HTML und bewegt das <article> Element
    an oberste Stelle
    """


current_ver = readVer()
updateVer(current_ver)
