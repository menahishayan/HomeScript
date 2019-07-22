#!/usr/bin/python

# HomeScript - Python script to control homebridge devices using the command line
# v3.0.1
# Created by Menahi Shayan. 2019.
# https://github.com/menahishayan/HomeScript

import requests
import sys
import json
import logging
from datetime import date

VERSION='3.0.1'

url = 'http://home.local:35945/'
headers = {'Content-Type': 'Application/json','authorization': '031-45-154',}

accessories={}
selectedAccessories=[]
selectedAccessoryNames={}
argumentLength = len(sys.argv)

exceptionFile='homescript_exception_' + date.today().strftime("%Y.%m.%d") + '.log'
logging.basicConfig(filename=exceptionFile,filemode = 'a', level=logging.DEBUG)

def getAccessories():
    global getAcc
    try:
        getAcc = requests.get(url + 'accessories', headers=headers)
        for item in getAcc.json()['accessories']:
            accessories.update({str(item['services'][1]['characteristics'][0]['value']) : {'aid':item['aid'],'iid':item['services'][1]['characteristics'][1]['iid'],'type':item['services'][0]['characteristics'][2]['value'],'value':item['services'][1]['characteristics'][1]['value']}})
    except:
        # print(sys.exc_info()[0])
        if sys.argv[1] == 'debug':
            # debugHandler(str(sys.exc_info()[0]))
            logging.error(Exception, exc_info=True)
            print 'Exception logged: ' + exceptionFile
    return accessories

def selectAccessory(inputName):
    try:
        for key in accessories:
            if inputName in key.lower():
                selectedAccessoryNames.update({accessories[key]['aid']:{'name':key}})
                selectedAccessories.append({'aid':accessories[key]['aid'], 'iid':accessories[key]['iid'], 'value':accessories[key]['value']})
    except:
        if sys.argv[1] == 'debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print 'Exception logged: ' + exceptionFile

def selectGroup(inputName):
    try:
        for key in accessories:
            if accessories[key]['type'].lower().startswith(inputName[:len(inputName)-2]):
                selectedAccessoryNames.update({accessories[key]['aid']:{'name':key}})
                selectedAccessories.append({'aid':accessories[key]['aid'], 'iid':accessories[key]['iid'], 'value':accessories[key]['value']})
    except:
        if sys.argv[1] == 'debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print 'Exception logged: ' + exceptionFile

def printAccessories(param=''):
    try:
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
    except:
        if sys.argv[1] == 'debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print 'Exception logged: ' + exceptionFile


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
    print '\n\t<accessory-name> : [EasyMatch Supported] toggles the accessory On or Off, or sets to value'
    print '\t\t\tUsage: python homeScript.py <accessory-name> [value]'
    print '\n\tall : sets value of multiple HomeKit accessories'
    print '\t\tUsage: python homeScript.py all <accessory-type> value'
    print '\t\t<accessory-type> : [EasyMatch Supported] sets all <accessory-type> to <value>'
    print '\n\tdebug : generates debug log file.'
    print '\t\tUsage: python homeScript.py debug <command>'
    print '\t\tEg: python homeScript.py debug all lights 0'
    print '\n\thelp : prints usage info'
    print '\nEg: python homeScript.py MainLight'
    print '    python homeScript.py bedlight 0'
    print '    python homeScript.py all lights 0'
    print '    python homeScript.py all switches 1'
    print '\nCreated by Menahi Shayan.\n'
    sys.exit()

def debugHandler(content='init'):
    if content=='init':
        debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "w")
        debugFile.write('HSDB: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log\nHSDB: HomeScript version: ' + VERSION)
        debugFile.write('\nHSDB: URL: ' + url + '\nHSDB: Headers: ' + json.dumps(headers))
        debugFile.write('\nHSDB: Accessories: ' + json.dumps(accessories))
        debugFile.write('\nHSDB: Selected accessories: ' + json.dumps(selectedAccessories))
        debugFile.write('\nHSDB: Selected accessory names: ' + json.dumps(selectedAccessoryNames))
        debugFile.write('\nHSDB: Arguments: ' + json.dumps(sys.argv))
        debugFile.write('\nHSDB: Get accessories response:\n' + getAcc.text + '\nHSDB: End get accessories response\n')
        debugFile.close()
    elif content=='end':
        debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
        debugFile.write('HSDB: End homeScript debug file')
        debugFile.close()
        print 'Debug logged: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log'
        sys.exit()
    else:
        debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
        debugFile.write('HSDB: ' + str(content) + '\n')
        debugFile.close()


if argumentLength==1:
    printHelp()

if sys.argv[1] == 'help':
    printHelp()

getAccessories()
argumentOffset=0

if sys.argv[1] == 'debug':
    argumentOffset=1

if sys.argv[1+argumentOffset] == 'list':
    printAccessories(sys.argv[2+argumentOffset] if argumentLength>(2+argumentOffset) else '')
    if sys.argv[1] == 'debug':
        debugHandler()
        debugHandler('end')
    sys.exit()
elif sys.argv[1+argumentOffset] == 'all':
    if argumentLength>(3+argumentOffset):
        selectGroup(sys.argv[2+argumentOffset].lower())
    else:
        printHelp()
else:
    selectAccessory(sys.argv[1+argumentOffset].lower())

if len(selectedAccessories) == 0:
    print 'Accessory/Group not found.\nHere are a list of accessories:\n'
    printAccessories('type')
    print '\nFor usage info type \'python homeScript.py help\''
    sys.exit()
else:
    for item in selectedAccessories:
        if argumentLength>(2+argumentOffset):
            item['value'] = sys.argv[argumentLength-1]
        elif item['value'] == 0 or item['value'] == False:
            item['value'] = '1'
        else:
            item['value'] = '0'
        selectedAccessoryNames[item['aid']].update({'value': item['value']})

setReq = requests.put(url + 'characteristics', headers=headers, data='{"characteristics":' + json.dumps(selectedAccessories) + '}')

if sys.argv[1] == 'debug':
    debugHandler()
    debugHandler('Set characteristics response:\n'+setReq.text)
    debugHandler('End set characteristics response')

try:
    for item in setReq.json()['characteristics']:
        print selectedAccessoryNames[item['aid']]['name'] + (' is ' + ('On' if selectedAccessoryNames[item['aid']]['value'] == '1' else 'Off')) if item['status'] == 0 else ('Error: ' + item['status'])
except:
    if sys.argv[1] == 'debug':
        # debugHandler(json.dumps(sys.exc_info()))
        logging.error(Exception, exc_info=True)
        print 'Exception logged: ' + exceptionFile

if sys.argv[1] == 'debug':
    debugHandler('end')
