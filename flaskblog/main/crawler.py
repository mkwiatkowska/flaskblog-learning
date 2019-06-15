import smtplib, re, urllib2, os.path, csv



response = urllib2.urlopen('https://www.notino.pl/lancome/la-vie-est-belle-en-rose-woda-toaletowa-dla-kobiet/')
html = response.read()