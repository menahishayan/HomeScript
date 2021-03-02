import argparse
import sys
from homescript import HomeScript

__HOSTNAME__='192.168.0.106'
__PORT__='51826'
__AUTH__='043-14-615'

argumentLength = len(sys.argv)

def printHelp():
	print('Usage: hs.py [option] [value]')
	print('Options:')
	print('  -l, --list    : Lists all available HomeKit accessories')
	print('                     Usage: hs.py -l [argument]')
	print('                     Arguments:')
	print('                         <none> : lists accessory names')
	print('                         aid : lists accessory names with AID value')
	print('                         iid : lists accessory names with IID value')
	print('                         id : lists accessory names with AID and IID')
	print('                         type : lists accessory names with type')
	print('                         value : lists accessory names current state\n')
	print('  -g, --get     :  [EasyMatch] gets current value of accessory')
	print('                     Usage: hs.py -g <accessory-name>\n')
	print('  -s, --set     :  [EasyMatch] toggles the accessory On or Off, or sets to value')
	print('                     Usage: hs.py -s <accessory-name> [value]\n')
	print('        all     :  Gets or sets value of multiple HomeKit accessories')
	print('                     Usage: hs.py -g all <accessory-type>')
	print('                            hs.py -s all <accessory-type> value\n')
	print('        <attrib>:  Sets value of accessory attribute')
	print('                     Usage: hs.py -s <accessory-name> <attribute> value')
	print('                            hs.py -s lifx -hue 250\n')
	print('  -d, --debug   : generates debug log file.')
	print('                     Usage: hs.py -d <command>')
	print('                     Eg: hs.py -d -s all lights 0\n')
	print('  -h, --help    : prints usage info\n')
	print('  -v, --version : prints HomeScript version\n')
	print('\nEg: hs.py -s MainLight')
	print('    hs.py -s bedlight 0')
	print('    hs.py -g all lights')
	print('    hs.py -s all switches 1')
	print('\nCreated by Menahi Shayan.\n')
	sys.exit()

parser = argparse.ArgumentParser(description='Command line control of HomeBridge',add_help=False)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-h', '--help', action='store_true')
parser.add_argument('-l', '--list', action='store',nargs='*')
parser.add_argument('-s', '--set', action='store', nargs=argparse.REMAINDER)
parser.add_argument('-g', '--get', action='store', nargs=argparse.REMAINDER)
parser.add_argument('-v', '--version', action='store_true')
args = parser.parse_args()

hs = HomeScript(__HOSTNAME__,__PORT__,__AUTH__, args.debug, sys.argv)

if argumentLength==1 or args.help:
	printHelp()

if args.version:
	hs.getVersion()
	sys.exit()

if args.list and len(args.list)>=0:
	hs.printAccessories(args.list[0] if len(args.list)>0 else '')
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
	print('\nFor usage info type \'hs.py -h\'')
	hs.debugHandler('end')
	sys.exit(-1)
else:
	if args.set:
		if '-b' not in args.set and '-hue' not in args.set and '-sat' not in args.set and '-t' not in args.set:
			hs.setStates(sys.argv[argumentLength-1] or None)
		else:
			if '-b' in args.set:
				hs.setValues('Brightness',sys.argv[argumentLength-1])
			elif '-hue' in args.set:
				hs.setValues('Hue',sys.argv[argumentLength-1])
			elif '-sat' in args.set:
				hs.setValues('Saturation',sys.argv[argumentLength-1])
			elif '-t' in args.set:
				hs.setValues('Color Temperature',sys.argv[argumentLength-1])

	elif args.get:
		hs.printSelectedItems()

	else:
		printHelp()

hs.debugHandler('end')