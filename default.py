import os,sys,urllib2
import xbmcplugin,xbmcgui
import xml.etree.ElementTree as ET

__addon__ = "SomaFM"
__addonid__ = "plugin.audio.somafm"
__version__ = "0.0.2"

def log(msg):
  print "[PLUGIN] '%s (%s)' " % (__addon__, __version__) + str(msg)

log("Initialized!")
log(sys.argv)

rootURL = "http://somafm.com/"

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
  url = rootURL + url
  log("Get HTML for URL: " + url)
  req = urllib2.Request(url, withData, getHeaders(withReferrer))
  response = urllib2.urlopen(req)
  data = response.read()
  response.close()
  return data
  
  
def addEntries():
    somaXML = getHTMLFor(url="channels.xml")
    channelsContainer = ET.fromstring(somaXML)

    for stations in channelsContainer.findall(".//channel"):
        title = stations.find('title').text
        img = rootURL + stations.find('image').text.replace(rootURL,"")
        url = rootURL + stations.find('fastpls').text.replace(rootURL,"")
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
