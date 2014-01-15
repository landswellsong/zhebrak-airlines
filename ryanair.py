#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ryanair support"""
from abstract_airline import *

class Ryanair(Airline):
    cookieURL="/SkySales/booking.aspx"
    cookieName="ASP.NET_SessionId"
    requestHost="www.bookryanair.com"
    requestURL="/SkySales/Search.aspx"
    needSSL=True
    
    def prepareFormData(self,fromIATA,toIATA,deptDate):
        return {    "__EVENTTARGET":"",
                    "SearchInput$IsFlexible":"on",
                    "SearchInput$TripType":"OneWay",
                    "SearchInput$Orig": fromIATA,
                    "SearchInput$Dest": toIATA,
                    "SearchInput$DeptDate":deptDate.strftime("%d/%m/%Y"),
                    "SearchInput$PaxTypeADT":1,            # TODO support nonadult passengers maybe?
                    "SearchInput$PaxTypeCHD":0,
                    "SearchInput$PaxTypeINFANT":0,
                    "formaction":"Search.aspx" }

X=Ryanair().getFlights("DTM","OPO",date(date.today().year, 2, 24))
fp=open("/tmp/out.html","w")
fp.write(X.read())
fp.close()
#Ryanair().doRequest({"ADULT":"1","CHILD":"0","INFANT":"0","culture":"gb","date1":"20140217","date2":"20140218","language":"","m1":"20140217aDTMOPO","m1DO":"0","m1DP":"0","m2":"20140218OPOaDTM","m2DO":"0","m2DP":"0","mode":"0","module":"SB","nom":"2","oP":"","pM":"0","pT":"1ADULT","page":"SELECT","rP":"","sector1_d":"OPO","sector1_o":"aDTM","sector_1_d":"17","sector_1_m":"022014","sector_2_d":"18","sector_2_m":"022014","tc":"1","travel_type":"on","acceptTerms":"yes"})

