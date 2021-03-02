# HomeScript - Python script to control homebridge devices using the command line
# v5.1
# Created by Menahi Shayan. 2019.
# https://github.com/menahishayan/HomeScript

import requests
import json
import logging
from datetime import date
# to add webcolors

__version__ = "5.2"

class HomeScript:
	def __init__(self,hostname,port, auth, debug=None, argv=None):
		self.__version__ = '5.2'
		self.url = 'http://' + hostname + ':' + str(port) + '/'
		self.headers = {'Content-Type': 'Application/json', 'authorization': auth}

		self.accessories={}
		self.selectedAccessories=[]
		self.selectedAccessoryNames={}

		self.getAccessories()

		self.debug = debug
		self.exceptionFile='homescript_exception_' + date.today().strftime("%Y.%m.%d") + '.log'
		if self.debug:
			self.debugHandler('init',argv)

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
			if self.debug:
				logging.error(Exception, exc_info=True)
			print('Exception logged: ' + self.exceptionFile)
		return self.accessories

	def selectAccessory(self,inputName):
		try:
			for key in self.accessories:
				if inputName in key.lower():
					self.selectedAccessoryNames.update({self.accessories[key]['aid']:{'name':key}})
					self.selectedAccessories.append({'aid':self.accessories[key]['aid'], 'value':self.accessories[key]['value']})
			return self.selectedAccessories
		except:
			if self.debug:
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + self.exceptionFile)

	def selectGroup(self,inputName):
		try:
			for key in self.accessories:
				if self.accessories[key]['type'].lower().startswith(inputName[:len(inputName)-2]):
					self.selectedAccessoryNames.update({self.accessories[key]['aid']:{'name':key}})
					self.selectedAccessories.append({'aid':self.accessories[key]['aid'], 'iid':self.accessories[key]['iid'], 'value':self.accessories[key]['value']})
			return self.selectedAccessories
		except:
			if self.debug:
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + self.exceptionFile)

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
			if self.debug:
				# debugHandler(json.dumps(sys.exc_info()))
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + self.exceptionFile)

	def getVersion(self):
		return self.__version__

	def getSelectedItems(self):
		return self.selectedAccessories

	def printSelectedItems(self):
		for item in self.selectedAccessories:
			print(self.selectedAccessoryNames[item['aid']]['name'] + ' ' + str(item['value']))

	def setStates(self,value):
		setData = []
		valueIndex = 0

		for item in self.selectedAccessories:
			if value.isdigit():
				item['value'][0]['value'] = int(value)
			elif item['value'][0]['value'] == 0 or item['value'][0]['value'] == False:
				item['value'][0]['value'] = 1
			else:
				item['value'][0]['value'] = 0

			self.selectedAccessoryNames[item['aid']].update({'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
			setData.append({'aid': item['aid'],'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
		setReq = requests.put(self.url + 'characteristics', headers=self.headers, data='{"characteristics":' + str(setData).replace('\'','\"') + '}')

		if self.debug:
			self.debugHandler('Set characteristics response:\n'+setReq.text)
			self.debugHandler('End set characteristics response')

		try:
			if setReq.status_code != 204:
				print(setReq)
				for item in setReq.json()['characteristics']:
					print(self.selectedAccessoryNames[item['aid']]['name'] + ' Error: ' + str(item['status']))
					return item['status']
		except:
			if self.debug:
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + self.exceptionFile)

	def setValues(self, attribute, value):
		setData = []
		valueIndex = 0

		for item in self.selectedAccessories:
			valueIndex = next((item['value'].index(v) for v in item['value'] if v['description'] == attribute), 0)

			if value.isdigit():
				if (int(value) <= item['value'][valueIndex]['maxValue']) and (int(value) >= item['value'][valueIndex]['minValue']) and (int(value)%item['value'][valueIndex]['minStep'] == 0):
					item['value'][valueIndex]['value'] = int(value)
				else:
					print('Error:\n   Max Value: ' + str(item['value'][valueIndex]['maxValue']) + '\n   Min Value: ' + str(item['value'][valueIndex]['minValue']) +  '\n   Min Step: ' + str(item['value'][valueIndex]['minStep']))
			# Increment/Decrement
			elif value.startswith('+') or value.startswith('-'):
				if int(value[1:])%item['value'][valueIndex]['minStep'] == 0:
					item['value'][valueIndex]['value'] += int(value[1:]) if value[0] == '+' else -int(value[1:])
				else:
					print('Error:\n   Max Value: ' + str(item['value'][valueIndex]['maxValue']) + '\n   Min Value: ' + str(item['value'][valueIndex]['minValue']) +  '\n   Min Step: ' + str(item['value'][valueIndex]['minStep']))
			elif item['value'][valueIndex]['value'] >= ((item['value'][valueIndex]['maxValue']-item['value'][valueIndex]['minValue'])/2) - (((item['value'][valueIndex]['maxValue']-item['value'][valueIndex]['minValue'])/2)%item['value'][valueIndex]['minStep']):
				item['value'][valueIndex]['value'] = item['value'][valueIndex]['maxValue']
			else:
				item['value'][valueIndex]['value'] = item['value'][valueIndex]['minValue']

			self.selectedAccessoryNames[item['aid']].update({'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
			setData.append({'aid': item['aid'],'iid': item['value'][valueIndex]['iid'], 'value': item['value'][valueIndex]['value']})
		setReq = requests.put(self.url + 'characteristics', headers=self.headers, data='{"characteristics":' + str(setData).replace('\'','\"') + '}')

		if self.debug:
			self.debugHandler('Set characteristics response:\n'+setReq.text)
			self.debugHandler('End set characteristics response')

		try:
			if setReq.status_code != 204:
				print(setReq)
				for item in setReq.json()['characteristics']:
					print(self.selectedAccessoryNames[item['aid']]['name'] + ' Error: ' + str(item['status']))
					return item['status']
		except:
			if self.debug:
				logging.error(Exception, exc_info=True)
				print('Exception logged: ' + self.exceptionFile)

	def debugHandler(self,content='init',argv=''):
		if content=='init':
			logging.basicConfig(filename=self.exceptionFile,filemode = 'a',encoding='utf-8', level=logging.DEBUG)
			debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "w")
			debugFile.write('HSDB: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log\nHSDB: HomeScript version: ' + self.__version__)
			debugFile.write('\nHSDB: URL: ' + self.url + '\nHSDB: Headers: ' + json.dumps(self.headers))
			debugFile.write('\nHSDB: Accessories: ' + json.dumps(self.accessories))
			debugFile.write('\nHSDB: Selected accessories: ' + json.dumps(self.selectedAccessories))
			debugFile.write('\nHSDB: Selected accessory names: ' + json.dumps(self.selectedAccessoryNames))
			debugFile.write('\nHSDB: Arguments: ' + json.dumps(argv))
			debugFile.write('\nHSDB: Get accessories response:\n' + str(getAcc) + '\nHSDB: End get accessories response\n')
		elif content=='end':
			debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
			debugFile.write('HSDB: End homeScript debug file')
			print('Debug logged: homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log')
		else:
			debugFile=open('homescript_debug_' + date.today().strftime("%Y.%m.%d") + '.log', "a")
			debugFile.write('HSDB: ' + str(content) + '\n')
		debugFile.close()

	def __del__(self):
		try:
			if self.debug:
				self.debugHandler('end')
		except:
			None
