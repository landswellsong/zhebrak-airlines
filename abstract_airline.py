#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Abstract class encapsulating basic functionality"""

import httplib,HTMLParser,re,urllib
from contextlib import closing
import time
from datetime import date

class Airline(HTMLParser.HTMLParser):
    # The following should be defined
    # requestHost       host to connect to
    needSSL=False     # whether to use SSL or not
    needCookies=False # whether or not to get and use a session cookie
    # cookieURL         the URL to obtain cookie from
    # cookieName        the session cookie name
    # requestURL        the request where to cather flight info
    # prepareFormData   method to convert the logical search terms into the form to send
    # parseResponse     method to parse the resonce data into flight list
    
    def __init__(self):
        if self.needCookies:
            self.cookieRegex=re.compile(self.cookieName+"=([^;]+)")
    
    def getCookie(self):
        '''Get and store the session cookie'''
        for i in self.doRequest(self.cookieURL,{},"GET",True).getheaders():
            if i[0]=="set-cookie":
                catch=self.cookieRegex.match(i[1])
                if catch is not None:
                    self.cookie=catch.group(1)
       
    def doGeneralRequest(self,ssl,method,host,url,params,headers={}):
        '''Very abstarct static-like method to run a general HTTP(S) request'''
        hdrs={"Content-type": "application/x-www-form-urlencoded","Accept": "text/html"}
        hdrs.update(headers)
        with closing((httplib.HTTPSConnection if ssl else httplib.HTTPConnection)(host)) as conn:
            conn.request(method,url,
                urllib.urlencode(params),
                hdrs)
            return conn.getresponse()
           
    def doRequest(self,url,params,method="POST",noCookie=False):
        '''Do the request against the known server and HTTPS settings'''
        cookies={}
        # TODO cookie code is broken, fugly and kill
        # I realized I don't need it for ryanair anyway
        if not noCookie and self.needCookies:
            if not hasattr(self,"cookie"):
                self.getCookie()
            #cookies[self.cookieName]=self.cookie TODO for now we assume only one session cookie
            # TODO probably we need to escape 'em but it's a stub code
            cookies={"Cookie": self.cookieName + "=" + self.cookie + ";"}
            
        rs=self.doGeneralRequest(self.needSSL,"POST",self.requestHost,url,params,cookies)
        if rs.status!=200 and rs.status!=302:
            raise Exception("Server reported code: ",rs.status)
        return rs
         
    def getFlights(self,fromIATA,toIATA,deptDate,strict=False): # TODO and the overloads of thereof
        '''Requests the list of flights from the given IATA to another one on a given date.
           If strict is set, only single day flights are returned, everything the airline outputted otherwise'''
        rs=self.doRequest(self.requestURL,self.prepareFormData(fromIATA,toIATA,deptDate))
        return self.parseResponse(rs.read())

