#!/usr/bin/env python3
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
import requests
import xml.etree.ElementTree as ET
from lxml import html

zillow_service = 'http://www.zillow.com/webservice/GetZestimate.htm'
trulia_service = 'http://api.trulia.com/webservices.php'

config = configparser.ConfigParser()

# Either of the following read methods work
#config.read_file(open('homevalue.ini'))
config.read('homevalue.ini')

def get_zillow_estimate_iter_test():
    key = config.get('zillow', 'api_key')
    houseCode = config.get('zillow', 'property_id')
    
    request = urllib.request.urlopen(zillow_service + "?zws-id=" + key + "&zpid=" + houseCode)
    data = request.read()
    
    f = open('housedata.xml', 'wb')
    f.write(data)
    f.close()

    #ET.parse() creates an ElementTree
    tree1 = ET.parse('housedata.xml')
    root = tree1.getroot()

    #ET.fromstring() creats an Element
    #this element is equivalent to the root of the above ElementTree
    tree2 = ET.fromstring(data)

    print("Tree1: " + str(type(tree1)))
    print("Tree2: " + str(type(tree2)))
    
    print()
    print(ET.tostring(root))
    

    for element in root:
        print(element.tag)
        for child in element:
            print(child.tag, child.attrib, child.text)
    
    print()
    print("now the iter")
    for value in root.iter('amount'):
        print(value.text)

def get_zillow_estimate():
    key = config.get('zillow', 'api_key')
    houseCode = config.get('zillow', 'property_id')
    
    request = urllib.request.urlopen(zillow_service + "?zws-id=" + key + "&zpid=" + houseCode)
    data = request.read()
    
    root = ET.fromstring(data)

    for amount in root.iter('amount'):
        print("Zillow: " + str(amount.text))

def get_trulia_estimate():
    url = config.get('trulia', 'home_url')

    page = requests.get(url)
    tree = html.fromstring(page.content)

    value = tree.xpath('//span[@itemprop="price"]/text()')

    print("Trulia: "+ str(value[0]))

get_zillow_estimate()
get_trulia_estimate()
