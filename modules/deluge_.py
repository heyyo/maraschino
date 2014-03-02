import traceback
import sys
import os
#import cherrypy
#import htpc
import urllib2
import gzip
import socket
from json import loads, dumps
import logging
import cookielib
from StringIO import StringIO

class Deluge:

    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

    def connected(self):
        return self.fetch('web.connected')   

    def connect(self,hostid):
        return self.fetch('web.connect',[hostid])


    def get_hosts(self):
        return self.fetch('web.get_hosts')


    def queue(self):
        fields = ['progress','is_finished','ratio','name','download_payload_rate','upload_payload_rate','eta','state','hash','total_size']
        return self.fetch('core.get_torrents_status', [[],fields])


    def stats(self):
        fields = ["payload_download_rate","payload_upload_rate"]
        return self.fetch('core.get_session_status',[fields])

    
    def start(self, torrentId):
        torrents = [torrentId]
        return self.fetch('core.resume_torrent', [torrents])

  
    def stop(self, torrentId):
        torrents = [torrentId]
        return self.fetch('core.pause_torrent',[torrents])

    
    def remove(self, torrentId, removeData):
        removeDataBool = bool(removeData);
        return self.fetch('core.remove_torrent', [torrentId,removeDataBool])

    # Wrapper to access the Deluge Api
    # If the first call fails, there probably is no valid Session ID so we try it again
    def fetch(self, method, arguments=[]):
        """ Do request to Deluge api """
        ##.debug("Request deluge method: "+method)

        # format post data
        data = {'id':1,'method': method,'params':arguments}
           
    
        response = self.read_data(data)
        print response
        ##.debug ("response is %s" %response)
        if response and response['error']:
            self.auth()
            response = self.read_data(data)
            ##.debug ("response is %s" %response)
        return response

    def auth(self):
        self.read_data({"method": "auth.login","params": ['deluge'],"id": 1})
        #self.read_data({"method": "auth.login","params": [htpc.settings.get('deluge_password', '')],"id": 1})

        
    def read_data(self,data):
        try:
            host = '192.168.1.122'
            port = '8112'

            url = 'http://' +  host + ':' + str(port) + '/json'
            
            post_data = dumps(data)
            buf = StringIO( self.opener.open(url, post_data,1).read())
            f = gzip.GzipFile(fileobj=buf)
            response = loads(f.read())
            #.debug ("response for %s is %s" %(data,response))
            #print response
            return response
        except urllib2.URLError:
            #.error ("can't connect with %s" %data)
            return {'result':{},'error':"can't connect with %s" %data}
        except socket.timeout:
            #.error ("timeout when connect with %s" %data)
            return {'result':{},'error':"can't connect with %s" %data}

client = Deluge()
#print dir(client)
#print client.auth()
client.get_hosts()
client.connect('213b2fcf523662859b077bbe2c40cb946764803f')
client.connected()
client.queue()
client.fetch('web.update.ui', '')