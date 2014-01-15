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
    # cookieURL         the URL to obtain cookie from
    # cookieName        the session cookie name
    # requestURL        the request where to cather flight info
    # prepareFormData   method to convert the logical search terms into the form to send
    cookie=""
    
    def __init__(self):
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
        hdrs={"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        hdrs.update(headers)
        with closing((httplib.HTTPSConnection if ssl else httplib.HTTPConnection)(host)) as conn:
            conn.request(method,url,
                urllib.urlencode(params),
                hdrs)
            return conn.getresponse()

    def doGeneralRequest2(self,ssl,method,host,url,params,headers={}):
        '''Very abstarct static-like method to run a general HTTP(S) request'''
        hdrs={
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie" :"drcn=15122013; ASP.NET_SessionId=regfbugjox55lggetry2luuqoe55; rateCodes=%7B%22en-IE%22%3A%22FOP%22%7D; s_vnum=1392323764269%26vn%3D2; drcsess=20860860450; New_Location=regf; s_cc=true; prevPage=website%3A%20ie%3A%20booking%3A%20search%3A%20none; s_nr=1389765742889-Repeat; s_invisit=true; s_sq=ryanairprod%3D%2526pid%253Dwebsite%25253A%252520ie%25253A%252520booking%25253A%252520search%25253A%252520none%2526pidt%253D1%2526oid%253DSEARCH%2526oidt%253D3%2526ot%253DSUBMIT",
            "Origin":"https://www.bookryanair.com",
            "Referer":"https://www.bookryanair.com/SkySales/booking.aspx",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
            }
        params={
            "__EVENTTARGET":"SearchInput$ButtonSubmit",
            "__EVENTARGUMENT":"",
            "__VIEWSTATE":"/wEPDwUBMGRkjfAE8Z7HGAsG5iDKx5dFCby0omY=",
            "formaction":"Search.aspx",
            "errorlist":"",
            "SearchInput$IsFlexible":"on",
            "SearchInput$TripType":"OneWay",
            "SearchInput$Orig":"DTM",
            "SearchInput$Dest":"OPO",
            "SearchInput$DeptDate":"24/02/2014",
            "SearchInput$RetDate":"24/02/2014",
            "SearchInput$PaxTypeADT":"1",
            "SearchInput$PaxTypeCHD":"0",
            "SearchInput$PaxTypeINFANT":"0"
            }
        with closing((httplib.HTTPSConnection if ssl else httplib.HTTPConnection)(host)) as conn:
            conn.request(method,url,
                urllib.urlencode(params),
                hdrs)
            return conn.getresponse()
 
            
    def doRequest(self,url,params,method="POST",noCookie=False):
        '''Do the request against the known server and HTTPS settings'''
        cookies={}
        if not noCookie:
            if not hasattr(self,"cookie"):
                self.getCookie()
            #cookies[self.cookieName]=self.cookie TODO for now we assume only one session cookie
            # TODO probably we need to escape 'em but it's a stub code
            cookies={"Cookie": self.cookieName + "=" + self.cookie + ";"} 
        rs=self.doGeneralRequest(self,self.needSSL,self.requestHost,url,params,cookies)
        if rs.status!=200 and rs.status!=302:
            raise Exception("Server reported code: ",rs.status)
        return rs
    
    def doRequest2(self,url,params,method="POST",noCookie=False):
        '''Do the request against the known server and HTTPS settings'''
        cookies={}
        if not noCookie:
            if not hasattr(self,"cookie"):
                self.getCookie()
            #cookies[self.cookieName]=self.cookie TODO for now we assume only one session cookie
            # TODO probably we need to escape 'em but it's a stub code
            cookies={"Cookie": self.cookieName + "=" + self.cookie + ";"} 
        rs=self.doGeneralRequest2(self,self.needSSL,self.requestHost,url,params,cookies)
        if rs.status!=200 and rs.status!=302:
            raise Exception("Server reported code: ",rs.status)
        return rs
        
    def getFlights(self,fromIATA,toIATA,deptDate,strict=False): # TODO and the overloads of thereof
        '''Requests the list of flights from the given IATA to another one on a given date.
           If strict is set, only single day flights are returned, everything the airline outputted otherwise'''
        return self.doRequest2(self.requestURL,self.prepareFormData(fromIATA,toIATA,deptDate))

