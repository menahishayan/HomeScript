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
# to add webcolors

VERSION='5.0'

# Change the parameters below for your HomeBridge
hostname = '192.168.0.6'
port = '35945'
auth = '031-45-154'

# End parameters

# Start of definitions
url = 'http://' + hostname + ':' + str(port) + '/'
headers = {'Content-Type': 'Application/json', 'authorization': auth}

accessories={}
selectedAccessories=[]
selectedAccessoryNames={}
argumentLength = len(sys.argv)

exceptionFile='homescript_exception_' + date.today().strftime("%Y.%m.%d") + '.log'

def getAccessories():
	global getAcc
	try:
		getAcc = requests.get(url + 'accessories', headers=headers)
		if getAcc.status_code == 200:
			getAcc = getAcc.json()
		# load sample data for debugging
		# with open('acc.json') as f:
		#   data = json.load(f)
		for item in getAcc['accessories']:
			if getAcc['accessories'].index(item) != 0:
				interfaces = []
				for i in item['services'][1]['characteristics'][1:]:
					if i['format'] not in ['bool','string','tlv8', 'uint8']:
						interfaces.append({'iid':i['iid'],'description': i['description'],'maxValue': i['maxValue'],'minValue': i['minValue'],'minStep': i['minStep'], 'value': i['value']})
					else:
						interfaces.append({'iid':i['iid'],'description': i['description'],'value': i['value']})
				accessories.update({str(item['services'][0]['characteristics'][3]['value']).replace(' ','_') : {'aid':item['aid'],'iid':10,'type':item['services'][0]['characteristics'][2]['value'],'value':interfaces}})

	except:
		if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
			logging.error(Exception, exc_info=True)
		print('Exception logged: ' + exceptionFile)
	return accessories

def selectAccessory(inputName):
	try:
		for key in accessories:
			if inputName in key.lower():
				selectedAccessoryNames.update({accessories[key]['aid']:{'name':key}})
				selectedAccessories.append({'aid':accessories[key]['aid'], 'value':accessories[key]['value']})
	except:
		if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
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
			print(key, end=' ')
			if param == 'type' or param == 'all':
				print(str(accessories[key]['type']) + ' ', end='')
			if param in ['value','iid','all']:
				# print(str(accessories[key]['value']), end='')
				for i in accessories[key]['value']:
					print('\n   ', end='')
					if param == 'iid' or param == 'all':
						print(str(i['iid']) + ' ' + str(i['value']), end=' ')
					if param == 'value' or param == 'all':
						print(str(i['description']) + ' ' + str(i['value']), end='')
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
		debugFile.write('\nHSDB: Get accessories response:\n' + str(getAcc) + '\nHSDB: End get accessories response\n')
	elif content=='end':
		debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
		debugFile.write('HSDB: End homeScript debug file')
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
		setData = []
		valueIndex = 0

		for item in selectedAccessories:
			if sys.argv[argumentLength-2] not in ['-b', '-h', '-sat', '-t', '--brightness', '--hue', '--saturation', '--temperature'] and sys.argv[argumentLength-1] not in ['-b', '-h', '-sat', '-t', '--brightness', '--hue', '--saturation', '--temperature']:
				if sys.argv[argumentLength-1].isdigit():
					item['value'][0]['value'] = sys.argv[argumentLength-1]
				elif item['value'][0]['value'] == 0 or item['value'][0]['value'] == False:
					item['value'][0]['value'] = '1'
				else:
					item['value'][0]['value'] = '0'
			else:

				if sys.argv[argumentLength-2] in ['-b', '--brightness'] or sys.argv[argumentLength-1] in ['-b', '--brightness']:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Brightness'), 0)
				elif sys.argv[argumentLength-2] in ['-h', '--hue'] or sys.argv[argumentLength-1] in ['-h', '--hue']:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Hue'), 0)
				elif sys.argv[argumentLength-2] in ['-sat', '--saturation'] or sys.argv[argumentLength-1] in ['-sat', '--saturation']:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Saturation'), 0)
				elif sys.argv[argumentLength-2] in ['-t', '--temperature'] or sys.argv[argumentLength-1] in ['-t', '--temperature']:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Color Temperature'), 0)

				if sys.argv[argumentLength-1].isdigit():
					if (int(sys.argv[argumentLength-1]) <= item['value'][valueIndex]['maxValue']) and (int(sys.argv[argumentLength-1]) >= item['value'][valueIndex]['minValue']) and (int(sys.argv[argumentLength-1])%item['value'][valueIndex]['minStep'] == 0):
						item['value'][valueIndex]['value'] = int(sys.argv[argumentLength-1])
					else:
						print('Error:\n   Max Value: ' + str(item['value'][valueIndex]['maxValue']) + '\n   Min Value: ' + str(item['value'][valueIndex]['minValue']) +  '\n   Min Step: ' + str(item['value'][valueIndex]['minStep']))
				elif item['value'][valueIndex]['value'] >= ((item['value'][valueIndex]['maxValue']-item['value'][valueIndex]['minValue'])/2) - (((item['value'][valueIndex]['maxValue']-item['value'][valueIndex]['minValue'])/2)%item['value'][valueIndex]['minStep']):
					item['value'][valueIndex]['value'] = item['value'][valueIndex]['maxValue']
				else:
					item['value'][valueIndex]['value'] = item['value'][valueIndex]['minValue']

			selectedAccessoryNames[item['aid']].update({'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
			setData.append({'aid': item['aid'],'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
		setReq = requests.put(url + 'characteristics', headers=headers, data='{"characteristics":' + str(setData).replace('\'','\"') + '}')

		if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
			debugHandler()
			debugHandler('Set characteristics response:\n'+setReq.text)
			debugHandler('End set characteristics response')

		try:
			if setReq.status_code != 204:
				print(setReq)
				for item in setReq.json()['characteristics']:
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
