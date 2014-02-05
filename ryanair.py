#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ryanair support"""
from abstract_airline import *
from datetime import datetime
import json

class Ryanair(Airline):
    requestHost="www.bookryanair.com"
    requestURL="/SkySales/Search.aspx"
    needSSL=True
    
    def prepareFormData(self,fromIATA,toIATA,deptDate):
        return {    "__EVENTTARGET":"SearchInput$ButtonSubmit",
                    "SearchInput$TripType":"OneWay",
                    "SearchInput$Orig": fromIATA,
                    "SearchInput$Dest": toIATA,
                    "SearchInput$DeptDate":deptDate.strftime("%d/%m/%Y"),
                    "SearchInput$PaxTypeADT":1,            # TODO support nonadult passengers maybe?
                    "SearchInput$PaxTypeCHD":0,
                    "SearchInput$PaxTypeINFANT":0 }
    
    def parseResponse(self,resp):
        # TODO is it safe to assume no ; happen in between?
        # TODO compile the regexp probably?
        m=re.search("FR.flightData = ({[^;]+});",resp)
        # TODO if blah blah blah not found
        flightData=json.loads(m.group(1))
        #We should get all flights for each day not only the first one
        for entry in flightData[flightData.keys()[0]]:
            while len(entry[1][i][2]) > 0 :    
                i=0
                yield {     "Flight":entry[1][i][2],
                            "From":flightData.keys()[0][0:3],
                            "To":flightData.keys()[0][3:6],
                            "Departure":datetime.strptime(entry[1][i][3][0][0]+" "+entry[1][i][3][0][1],"%Y-%m-%d %H:%M"),
                            "Arrival":datetime.strptime(entry[1][i][3][1][0]+" "+entry[1][i][3][1][1],"%Y-%m-%d %H:%M"),
                            "Price":entry[1][i][4]['ADT'][1]['FarePrice'],
                            "Tax":entry[1][i][4]['ADT'][1]['Tax'] }
                i=i+1
                #hack to break the loop, number of daily flights are unknown
				try:
					len(entry[1][i][2])
				except :
					break

# Testin'
for entry in Ryanair().getFlights("DTM","OPO",date(2014, 3, 24)):
    print "Flight:\t"+entry["Flight"]+" "+entry["From"]+u"→"+entry["To"]
    print "\tDeparture:\t"+str(entry["Departure"])
    print "\tArrival:\t"+str(entry["Arrival"])
    print "\tPrice:\t\t"+str(entry["Price"]+entry["Tax"])+"("+str(entry["Price"])+"+"+str(entry["Tax"])+")"

