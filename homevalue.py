#!/usr/bin/python3.4
#
# 09/23/2015
#
# A python application that returns the zillow and trulia home value estimate of a given property
#
# A zillow and trulia api key are required to be present in homevalue.ini file
#

import os
import configparser
import urllib.request
import xml.etree.ElementTree as ET

zillow_service = 'http://www.zillow.com/webservice/GetZestimate.htm'
trulia_service = 'http://api.trulia.com/webservices.php'

config = configparser.ConfigParser()

# Either of the following read methods work
#config.read_file(open('homevalue.ini'))
config.read('homevalue.ini')

def get_zillow_estimate():
    key = config.get('zillow', 'api_key')
    houseCode = config.get('zillow', 'property_id')
    
    request = urllib.request.urlopen(zillow_service + "?zws-id=" + key + "&zpid=" + houseCode)
    data = request.read()
    f = open('housedata.xml', 'wb')
    f.write(data)
    f.close()

    tree = ET.parse('housedata.xml')
    root = tree.getroot()

    for element in root:
        print(element.tag, element.attrib)

get_zillow_estimate()
