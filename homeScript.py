#!/usr/bin/python

# HomeScript - Python script to control homebridge devices using the command line
# v2.1
# Created by Menahi Shayan. 2019.

import requests
import sys
import json

url = 'http://home.local:35945/'
headers = {'Content-Type': 'Application/json','authorization': '031-45-154',}

accessories={}

def getAccessories():
    getAcc = requests.get(url + 'accessories', headers=headers)
    for item in getAcc.json()['accessories']:
#        accessories.append({'aid':item['aid'],'iid':item['services'][1]['characteristics'][1]['iid'],'name':item['services'][1]['characteristics'][0]['value'],'value':item['services'][1]['characteristics'][1]['value']})
        accessories.update({str(item['services'][1]['characteristics'][0]['value']) : {'aid':item['aid'],'iid':item['services'][1]['characteristics'][1]['iid'],'type':item['services'][0]['characteristics'][2]['value'],'value':item['services'][1]['characteristics'][1]['value']}})
    return accessories

def selectAccessory(inputName):
    global accessoryName
    for key in accessories:
        if inputName in key.lower():
            accessoryName = key
            return accessories[key]
    return {'aid':-1, 'iid':-1, 'type':'null', 'value': -1}

def printAccessories(param=''):
    if param == 'json':
        print json.dumps(accessories)
        return
    for key in accessories:
        if param == 'aid':
            print str(accessories[key]['aid']) + ' ',
        if param == 'iid':
            print str(accessories[key]['iid']) + ' ',
        if param == 'id' or param == 'all':
            print str(accessories[key]['aid']) + '.' + str(accessories[key]['iid']) + ' ',
        print key,
        if param == 'type' or param == 'all':
            print str(accessories[key]['type']) + ' ',
        if param == 'value' or param == 'all':
            print str(accessories[key]['value']),
        print ''

def printHelp():
    print 'Usage: python homeScript.py [option] [value]'
    print 'Options:'
    print '\n\tlist : lists all available HomeKit accessories'
    print '\t\tUsage: python homeScript.py list [argument]'
    print '\t\tArguments:'
    print '\t\t\t<none> : lists accessory names'
    print '\t\t\taid : lists accessory names with AID value'
    print '\t\t\tiid : lists accessory names with IID value'
    print '\t\t\tid : lists accessory names with AID and IID'
    print '\t\t\ttype : lists accessory names with type'
    print '\t\t\tvalue : lists accessory names current state'
    print '\n\t<accessory-name> : toggles the accessory On or Off, or sets to value'
    print '\t\t\tUsage: python homeScript.py <accessory-name> [value]'
    print '\n\thelp : prints usage info'
    print '\nEg: python homeScript.py MainLight'
    print '    python homeScript.py main 0'
    print '\nCreated by Menahi Shayan.\n'
    sys.exit()

if len(sys.argv)==1:
    printHelp()

if sys.argv[1] == 'help':
    printHelp()

getAccessories()

if sys.argv[1] == 'list':
    printAccessories(sys.argv[2] if len(sys.argv)>2 else '')
    sys.exit()

obj = selectAccessory(sys.argv[1].lower())

if obj['aid'] == -1:
    print 'Accessory not found.\nHere are a list of accessories:\n'
    printAccessories()
    print '\nFor usage info type \'python homeScript.py help\''
    sys.exit()

if len(sys.argv)>2:
    setVal = str(sys.argv[2])
elif obj['value'] == True:
    setVal = '0'
else:
    setVal = '1'

setReq = requests.put(url + 'characteristics', headers=headers, data='{"characteristics":[{"aid":' + str(obj['aid']) + ',"iid":' + str(obj['iid']) + ',"value":' + setVal + '}]}')

if setReq.json()['characteristics'][0]['status'] == 0:
    print accessoryName + ' is ' + ('On' if setVal == '1' else 'Off')
else:
    print 'An error occurred'
