km-rss-feed
===========

## Aufgabenstellung
Es geht darum einen RSS Feed und eine Newsseite, die jeweils als File auf einem Webserver liegen, so zu editieren, dass die jeweils aktuelle Version der Software des Kunden dort angezeigt wird. Später sollen noch Ausschnitte des Changelogs des Updates auf der Newsseite angezeigt werden.

### Dateistruktur:
- root
- -> Contents
- ---- ELBW.html
- ---- GLBW.html
- -> Support
- ---> RawBin
- ------ 14.03735.txt
- de.rss
- en.rss
- updates.php

### gewünschte Funktionalität:
- Die aktuellste Software Version soll aus Support/RawBin/*.txt ausgelesen werden
- die bereits gelesene Datei soll danach als 'verarbeitet' markiert werden, damit sie nicht noch einmal gelesen wird 
- die Datei soll aber nicht gelöscht werden (umbennen in .bak wäre eine Möglichkeit)
- beide RSS feeds sollen *ausschließlich* die aktuellste Version der Software enthalten (z.B. 14.03)
- andere, nicht Versionsrelevante Elemente müssen unverändert erhalten bleiben.
- RSS feeds sollen weiterhin [W3C valide](http://validator.w3.org/feed) sein.
- beide HTML Dateien (in Contents) sollen an entsprechender stelle *auschließlich* die aktuelle Version enthalten
- andere, nicht Versionsrelevante Elemente müssen unverändert erhalten bleiben.
- falls das entsprechende <article> element sich nicht an oberster/erster Stelle im DOM befindet, soll es dorthin verschoben werden

## Zusätzliche Features:
- Falls die Textdatei unter Support/RawBin/ den Status 'new' enthält, handelt es sich um ein neues Feature, dass im RSS und in den HTML Files im Text aufgelistet werden soll.
- Eine zusätzliche HTML Datei soll generiert werden, die alle Changelogs enthält, sortiert und categorisiert nach Versionsnummer. Dabei sollen alle im Verzeichnis vorhandenen Changelogs benutzt werden (auch die als 'verarbeitet' gekennzeichneten)
