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

import argparse
# to add webcolors

__version__ = '5.1'

argumentLength = len(sys.argv)
exceptionFile='homescript_exception_' + date.today().strftime("%Y.%m.%d") + '.log'

class HomeScript:
	def __init__(self,hostname,port, auth):
		self.url = 'http://' + hostname + ':' + str(port) + '/'
		self.headers = {'Content-Type': 'Application/json', 'authorization': auth}

		self.accessories={}
		self.selectedAccessories=[]
		self.selectedAccessoryNames={}

	def getAccessories(self):
		global getAcc
		try:
			getAcc = requests.get(self.url + 'accessories', headers=self.headers)
			if getAcc.status_code == 200:
				getAcc = getAcc.json()
			# load sample data for debugging
			# with open('acc.json') as f:
			#   data = json.load(f)
			for item in getAcc['accessories']:
				if getAcc['accessories'].index(item) != 0:
					interfaces = []
					for i in item['services'][1]['characteristics'][1:]:
						if i['format'] not in ['bool','string','tlv8','uint8','float']:
							interfaces.append({'iid':i['iid'],'description': i['description'],'maxValue': i['maxValue'],'minValue': i['minValue'],'minStep': i['minStep'], 'value': i['value']})
						else:
							interfaces.append({'iid':i['iid'],'description': i['description'],'value': i['value']})
					self.accessories.update({str(item['services'][0]['characteristics'][3]['value']).replace(' ','_') : {'aid':item['aid'],'iid':10,'type':item['services'][0]['characteristics'][2]['value'],'value':interfaces}})

		except:
			if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
				logging.error(Exception, exc_info=True)
			print('Exception logged: ' + exceptionFile)
		return self.accessories

	def selectAccessory(self,inputName):
		try:
			for key in self.accessories:
				if inputName in key.lower():
					self.selectedAccessoryNames.update({self.accessories[key]['aid']:{'name':key}})
					self.selectedAccessories.append({'aid':self.accessories[key]['aid'], 'value':self.accessories[key]['value']})
		except:
			if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + exceptionFile)

	def selectGroup(self,inputName):
		try:
			for key in self.accessories:
				if self.accessories[key]['type'].lower().startswith(inputName[:len(inputName)-2]):
					self.selectedAccessoryNames.update({self.accessories[key]['aid']:{'name':key}})
					self.selectedAccessories.append({'aid':self.accessories[key]['aid'], 'iid':self.accessories[key]['iid'], 'value':self.accessories[key]['value']})
		except:
			if sys.argv[1] == '-d' or sys.argv[1] == '--debug':
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + exceptionFile)

	def printAccessories(self,param=''):
		try:
			if param == 'json':
				print(json.dumps(self.accessories))
				return
			for key in self.accessories:
				if param == 'aid':
					print(str(self.accessories[key]['aid']) + ' ', end='')
				print(key, end=' ')
				if param == 'type' or param == 'all':
					print(str(self.accessories[key]['type']) + ' ', end='')
				if param in ['value','iid','all']:
					# print(str(self.accessories[key]['value']), end='')
					for i in self.accessories[key]['value']:
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

	def debugHandler(self,content='init'):
		if content=='init':
			debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "w")
			debugFile.write('HSDB: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log\nHSDB: HomeScript version: ' + __version__)
			debugFile.write('\nHSDB: URL: ' + self.url + '\nHSDB: Headers: ' + json.dumps(self.headers))
			debugFile.write('\nHSDB: Accessories: ' + json.dumps(self.accessories))
			debugFile.write('\nHSDB: Selected accessories: ' + json.dumps(self.selectedAccessories))
			debugFile.write('\nHSDB: Selected accessory names: ' + json.dumps(self.selectedAccessoryNames))
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

# End definitions

# Start main

hs = HomeScript('192.168.0.106','51826','043-14-615')

parser = argparse.ArgumentParser(description='Command line control of HomeBridge',add_help=False)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-h', '--help', action='store_true')
parser.add_argument('-l', '--list', action='store',nargs='*')
parser.add_argument('-s', '--set', action='store', nargs=argparse.REMAINDER)
parser.add_argument('-g', '--get', action='store', nargs=argparse.REMAINDER)
parser.add_argument('-v', '--version', action='store_true')

args = parser.parse_args()

if argumentLength==1:
	printHelp()

if args.help:
	printHelp()

if args.version:
	print(__version__)
	sys.exit()

hs.getAccessories()

if args.debug:
	logging.basicConfig(filename=exceptionFile,filemode = 'a',encoding='utf-8', level=logging.DEBUG)
	hs.debugHandler()

if args.list and len(args.list)>=0:
	hs.printAccessories(args.list[0] if len(args.list)>0 else '')
	if args.debug:
		hs.debugHandler('end')
	sys.exit()
elif args.get and len(args.get)>=0:
	if args.get[0] == 'all':
		hs.selectGroup(args.get[1].lower())
	else:
		hs.selectAccessory(args.get[0].lower())
elif args.set and len(args.set)>=0:
	if args.set[0] == 'all':
		hs.selectGroup(args.set[1].lower())
	else:
		hs.selectAccessory(args.set[0].lower())

if len(hs.selectedAccessories) == 0:
	print('Accessory/Group not found.\nHere are a list of accessories:\n')
	hs.printAccessories('type')
	print('\nFor usage info type \'homeScript.py -h\'')
	sys.exit(-1)
else:
	if args.set:
		setData = []
		valueIndex = 0

		for item in hs.selectedAccessories:
			if '-b' not in args.set and '-hue' not in args.set and '-sat' not in args.set and '-t' not in args.set:
				if len(args.set)==2 and args.set[1].isdigit():
					item['value'][0]['value'] = int(args.set[1])
				elif item['value'][0]['value'] == 0 or item['value'][0]['value'] == False:
					item['value'][0]['value'] = 1
				else:
					item['value'][0]['value'] = 0
			else:
				if '-b' in args.set:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Brightness'), 0)
				elif '-hue' in args.set:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Hue'), 0)
				elif '-sat' in args.set:
					valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == 'Saturation'), 0)
				elif '-t' in args.set:
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

			hs.selectedAccessoryNames[item['aid']].update({'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
			setData.append({'aid': item['aid'],'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
		setReq = requests.put(hs.url + 'characteristics', headers=hs.headers, data='{"characteristics":' + str(setData).replace('\'','\"') + '}')

		if args.debug:
			hs.debugHandler()
			hs.debugHandler('Set characteristics response:\n'+setReq.text)
			hs.debugHandler('End set characteristics response')

		try:
			if setReq.status_code != 204:
				print(setReq)
				for item in setReq.json()['characteristics']:
					print(hs.selectedAccessoryNames[item['aid']]['name'] + ' Error: ' + str(item['status']))
					sys.exit(item['status'])
		except:
			if args.debug:
				# debugHandler(json.dumps(sys.exc_info()))
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + exceptionFile)

	elif args.get:
		for item in hs.selectedAccessories:
			print(hs.selectedAccessoryNames[item['aid']]['name'] + ' ' + str(item['value']))

	else:
		printHelp()

if args.debug:
	hs.debugHandler('end')