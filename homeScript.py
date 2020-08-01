#!/usr/local/bin/python3

# HomeScript - Python script to control homebridge devices using the command line
# v4.0
# Created by Menahi Shayan. 2019.
# https://github.com/menahishayan/HomeScript

import requests
import sys
import json
import logging
from datetime import date

VERSION='4.0'

# Change the parameters below for your HomeBridge
hostname = '192.168.0.6'
port = '35945'
auth = '031-45-154'

# End parameters

# Start of definitions
url = 'http://' + hostname + ':' + str(port) + '/'
headers = {'Content-Type': 'Application/json','authorization': auth}

accessories={}
selectedAccessories=[]
selectedAccessoryNames={}
argumentLength = len(sys.argv)

exceptionFile='homescript_exception_' + date.today().strftime("%Y.%m.%d") + '.log'


def getAccessories():
    global getAcc
    try:
        getAcc = requests.get(url + 'accessories', headers=headers)
        for item in getAcc.json()['accessories']:
            if getAcc.json()['accessories'].index(item) != 0:
	            accessories.update({str(item['services'][0]['characteristics'][3]['value']).replace(' ','_') : {'aid':item['aid'],'iid':10,'type':item['services'][0]['characteristics'][2]['value'],'value':item['services'][1]['characteristics'][1]['value']}})
    except:
        # print(sys.exc_info()[0])
        if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
            # debugHandler(str(sys.exc_info()[0]))
            logging.error(Exception, exc_info=True)
            print('Exception logged: ' + exceptionFile)
    return accessories

def selectAccessory(inputName):
    try:
        for key in accessories:
            if inputName in key.lower():
                selectedAccessoryNames.update({accessories[key]['aid']:{'name':key}})
                selectedAccessories.append({'aid':accessories[key]['aid'], 'iid':accessories[key]['iid'], 'value':accessories[key]['value']})
    except:
        if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print('Exception logged: ' + exceptionFile)

def selectGroup(inputName):
    try:
        for key in accessories:
            if accessories[key]['type'].lower().startswith(inputName[:len(inputName)-2]):
                selectedAccessoryNames.update({accessories[key]['aid']:{'name':key}})
                selectedAccessories.append({'aid':accessories[key]['aid'], 'iid':accessories[key]['iid'], 'value':accessories[key]['value']})
    except:
        if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print('Exception logged: ' + exceptionFile)

def printAccessories(param=''):
    try:
        if param == 'json':
            print(json.dumps(accessories))
            return
        for key in accessories:
            if param == 'aid':
                print(str(accessories[key]['aid']) + ' ', end='')
            if param == 'iid':
                print(str(accessories[key]['iid']) + ' ', end='')
            if param == 'id' or param == 'all':
                print(str(accessories[key]['aid']) + '.' + str(accessories[key]['iid']) + ' ', end='')
            print(key, end=' ')
            if param == 'type' or param == 'all':
                print(str(accessories[key]['type']) + ' ', end='')
            if param == 'value' or param == 'all':
                print(str(accessories[key]['value']), end='')
            print('')
    except:
        if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
            # debugHandler(json.dumps(sys.exc_info()))
            logging.error(Exception, exc_info=True)
            print('Exception logged: ' + exceptionFile)


def printHelp():
    print('Usage: homeScript.py [option] [value]')
    print('Options:')
    print('  -l, --list    : Lists all available HomeKit accessories')
    print('                     Usage: homeScript.py -l [argument]')
    print('                     Arguments:')
    print('                         <none> : lists accessory names')
    print('                         aid : lists accessory names with AID value')
    print('                         iid : lists accessory names with IID value')
    print('                         id : lists accessory names with AID and IID')
    print('                         type : lists accessory names with type')
    print('                         value : lists accessory names current state\n')
    print('  -g, --get     :  [EasyMatch] gets current value of accessory')
    print('                     Usage: homeScript.py -g <accessory-name>\n')
    print('  -s, --set     :  [EasyMatch] toggles the accessory On or Off, or sets to value')
    print('                     Usage: homeScript.py -s <accessory-name> [value]\n')
    print('        all     :  Gets or sets value of multiple HomeKit accessories')
    print('                     Usage: homeScript.py -g all <accessory-type>')
    print('                            homeScript.py -s all <accessory-type> value\n')
    print('  -d, --debug   : generates debug log file.')
    print('                     Usage: homeScript.py -d <command>')
    print('                     Eg: homeScript.py -d -s all lights 0\n')
    print('  -h, --help    : prints usage info\n')
    print('  -v, --version : prints HomeScript version\n')
    print('\nEg: homeScript.py -s MainLight')
    print('    homeScript.py -s bedlight 0')
    print('    homeScript.py -g all lights')
    print('    homeScript.py -s all switches 1')
    print('\nCreated by Menahi Shayan.\n')
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
        print('Debug logged: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log')
        sys.exit()
    else:
        debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
        debugFile.write('HSDB: ' + str(content) + '\n')
        debugFile.close()

# End definitions

# Start main

if argumentLength==1:
    printHelp()

if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
    logging.basicConfig(filename=exceptionFile,filemode = 'a', level=logging.DEBUG)

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    printHelp()

if sys.argv[1] == '-v' or sys.argv[1] == '--version':
    print(VERSION)
    sys.exit()

getAccessories()
argumentOffset=0

if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
    argumentOffset=1
    debugHandler()

if sys.argv[1+argumentOffset] == '-l' or sys.argv[1+argumentOffset] == '--list':
    printAccessories(sys.argv[2+argumentOffset] if argumentLength>(2+argumentOffset) else '')
    if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
        debugHandler('end')
    sys.exit()
elif sys.argv[2+argumentOffset] == 'all':
    if argumentLength>(3+argumentOffset + (1 if sys.argv[1+argumentOffset] == '-s' or sys.argv[1+argumentOffset] == '--set' else 0)):
        selectGroup(sys.argv[3+argumentOffset].lower())
    else:
        printHelp()
else:
    selectAccessory(sys.argv[2+argumentOffset].lower())

if len(selectedAccessories) == 0:
    print('Accessory/Group not found.\nHere are a list of accessories:\n')
    printAccessories('type')
    print('\nFor usage info type \'homeScript.py -h\'')
    sys.exit(-1)
else:
    if sys.argv[1+argumentOffset] == '-s' or sys.argv[1+argumentOffset] == '--set':
        for item in selectedAccessories:
            if argumentLength>(3+argumentOffset):
                item['value'] = sys.argv[argumentLength-1]
            elif item['value'] == 0 or item['value'] == False:
                item['value'] = '1'
            else:
                item['value'] = '0'
            selectedAccessoryNames[item['aid']].update({'value': item['value']})

            print('{"characteristics":' + json.dumps(selectedAccessories) + '}')
            setReq = requests.put(url + 'characteristics', headers=headers, data='{"characteristics":' + json.dumps(selectedAccessories) + '}')

            if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
                debugHandler()
                debugHandler('Set characteristics response:\n'+setReq.text)
                debugHandler('End set characteristics response')

            try:
                for item in setReq.json()['characteristics']:
                    #        print selectedAccessoryNames[item['aid']]['name'] + ' ',
                    #        if item['status'] == 0:
                    #            print str(selectedAccessoryNames[item['aid']]['value'])
                    #        else:
                    #            print 'Error: ' + item['status']
                    #            sys.exit(item['status'])
                    if item['status'] != 0:
                        print(selectedAccessoryNames[item['aid']]['name'] + ' Error: ' + str(item['status']))
                        sys.exit(item['status'])
            except:
                if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
                    # debugHandler(json.dumps(sys.exc_info()))
                    logging.error(Exception, exc_info=True)
                    print('Exception logged: ' + exceptionFile)

    elif sys.argv[1+argumentOffset] == '-g' or sys.argv[1+argumentOffset] == '--get':
        for item in selectedAccessories:
            print(selectedAccessoryNames[item['aid']]['name'] + ' ' + str(item['value']))

    else:
        printHelp()

if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
    debugHandler('end')

sys.exit()
