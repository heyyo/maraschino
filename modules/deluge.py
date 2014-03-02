# -*- coding: utf-8 -*-

import urllib2
import urllib
import gzip
import socket
from json import loads, dumps
import logging
import cookielib
from StringIO import StringIO
import os

'''
from jinja2.filters import FILTERS

from flask import Flask, jsonify, render_template
from Maraschino import app
from maraschino import logger
from maraschino.tools import *
'''
#cj = None

def deluge_http():
    if 1 == '1':
    #if get_setting_value('deluge_https') == '1':
        return 'https://'
    else:
        return 'http://'

def deluge_url():
    port = '8112'#get_setting_value('deluge_port')
    url_base = '192.168.1.122'#get_setting_value('deluge_ip')
    webroot = None #get_setting_value('deluge_webroot')
    
    if port:
        url_base= '%s:%s' % (url_base, port)
    
    if webroot:
        url_base = '%s/%s' % (url_base, webroot)
     
    url = '%s/json' % url_base
    
    return deluge_http() + url

def fetch(method, arguments=[]):
    # format post data
    data = {'id':1,'method': method,'params':arguments}
    
    response = read_data(data)
    print 'RR is : %s' % response
    
    print 'Response[error] %s' % response['error']
    
    #logger.log('qbittorrent :: There is a problem reaching qBittorrent', 'INFO')
    
    if response and response['error']:
        auth() # needs to have auth
        response = read_data(data)
        print 'crazy ass response %s' % response
        #self.logger.debug ("response is %s" %response)#
        #logger.log('qbittorrent :: There is a problem reaching Deluge', 'DEBUG')
    #print response
    return response

def auth():
    print 'Running auth'
    #read_data({"method": "auth.login","params": [get_settings_value('deluge_password')],"id": 1})
    read_data({"method": "auth.login","params": ['deluge'],"id": 1})

def _cookie():
    print 'RUNNING COOKIE'
    cj = cookielib.CookieJar()
    
    for cookie in cj:
        print cookie
        #cj = cookielib.LWPCookieJar()
    
def read_data(data):
    
    #cj= _cookie()
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    try:
        #cj = cookielib.CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #print 'Cookie', cj
        print 'Parameter sendt to read_data :: %s' % data
        #print opener.value
            

        #url = deluge_url()
        host = '192.168.1.122'
        port = '8112'
            

        url = 'http://' +  host + ':' + str(port) + '/json'
        print 'Url is : %s' % url
        
        post_data = dumps(data)
            
        print 'post data', post_data
            
        #buf = StringIO(x)
        buf = StringIO(opener.open(url, post_data,1).read())
        #print req.get_header('Content-Type')
        print 'Cookie awesome', cj
            
        f = gzip.GzipFile(fileobj=buf)
        #print 'f is : ',f.read()
          
        response = loads(f.read()) # need t his one
            
        print 'decoded response is : %s for command %s' % (response, data)
        return response
            
    except Exception as e:
        print e
        #print data#self.logger.error ("can't connect with %s" %data)
        return {'result':{},'error':"can't connect with %s" %data}
            
    except socket.timeout:
        #print data
        #self.logger.error ("timeout when connect with %s" %data)
        return {'result':{},'error':"can't connect with %s" %data}

#fetch('web.get_hosts', arguments=None)
#{"method": "auth.login","params": ['deluge'],"id": 1}

fetch('auth.login', ['deluge'])
fetch('web.get_hosts')
#fetch('web.get_torrent_files', [])