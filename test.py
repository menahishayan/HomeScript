import json

accessories = {}

with open('acc.json') as f:
  data = json.load(f)

nonIncrementableFormats = ['bool','string','tlv8', 'uint8']

print(str(data))

for item in data['accessories']:
	if data['accessories'].index(item) != 0:
		for i in item['services'][1]['characteristics'][1:]:
			if i['format'] not in nonIncrementableFormats :
				print(i['iid'], end=" ")
				print(i['description'], end=" ")
				print(i['maxValue'], end=" ")
				print(i['minValue'], end=" ")
				print(i['minStep'])
			else:
				print(i['iid'], end=" ")
				print(i['description'] + ' ' + str(i['value']))
		print('---')
	# accessories.update({str(item['services'][1]['characteristics'][0]['value'] or item['services'][0]['characteristics'][2]['value']).replace(' ','_') : {'aid':item['aid'],'iid':item['services'][1]['characteristics'][1]['iid'],'type':item['services'][0]['characteristics'][2]['value'],'value':item['services'][1]['characteristics'][1]['value']}})
