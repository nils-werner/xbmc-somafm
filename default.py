import os,urllib2,xbmcplugin,xbmcgui
#from cgi import parse_qs
from BeautifulSoup import BeautifulStoneSoup as Soup
#, BeautifulStoneSoup

__addon__ = "SomaFM"
__addonid__ = "plugin.audio.somafm"
__version__ = "0.0.1"

def log(msg):
  print "[PLUGIN] '%s (%s)' " % (__addon__, __version__) + str(msg)

log("Initialized!")
log(sys.argv)

rootURL = "http://somafm.com"

#pluginPath = sys.argv[0]
handle = int(sys.argv[1])
query = sys.argv[2]

def getHeaders(withReferrer=None):
  headers = {}
  headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'
  if withReferrer:
    headers['Referrer'] = withReferrer
  return headers

def getHTMLFor(url, withData=None, withReferrer=None):
  log("Get HTML for URL: " + url)
  req = urllib2.Request(url, withData, getHeaders(withReferrer))
  response = urllib2.urlopen(req)
  data = response.read()
  response.close()
  return data
  
  
def addEntries():
    somaHTML = getHTMLFor(url=rootURL)
    stationsDiv = Soup(somaHTML).find("div", id="stations")

    for stations in stationsDiv.findAll("li"):
        #log(stations.prettify())
        title = stations.h3.string
        img = rootURL + stations.img["src"]
        url = rootURL + stations.a["href"].replace("/play","") + ".pls"
        log(title)
        log(img)
        log(url)
        li = xbmcgui.ListItem(title, thumbnailImage=img)
        li.setProperty("IsPlayable","true")
        xbmcplugin.addDirectoryItem(
            handle=handle,
            url=url,
            listitem=li)


addEntries()            
xbmcplugin.endOfDirectory(handle)

#li = xbmcgui.ListItem("GrooveSalad")
#li.setProperty('IsPlayable', 'true')



