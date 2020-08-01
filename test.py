import json

accessories = {}

with open('acc.json') as f:
  data = json.load(f)

for item in data['accessories']:
	if data['accessories'].index(item) != 0:
		print(item['services'][1]['characteristics'][0]['iid'])
		print(item['services'][0]['characteristics'][3]['value'])
		print(item['services'][1]['characteristics'][1]['value'])
		print('---')
	# accessories.update({str(item['services'][1]['characteristics'][0]['value'] or item['services'][0]['characteristics'][2]['value']).replace(' ','_') : {'aid':item['aid'],'iid':item['services'][1]['characteristics'][1]['iid'],'type':item['services'][0]['characteristics'][2]['value'],'value':item['services'][1]['characteristics'][1]['value']}})
