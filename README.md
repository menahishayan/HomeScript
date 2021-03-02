# HomeScript
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/menahishayan)  

Python script for command line control of [HomeBridge](https://github.com/nfarina/homebridge) (HomeKit)

Used to toggle Homebridge accessories On or Off via python script, no Home app required. You can set up a cronjob to enable automation, scripting and mimic other HomeKit functionalities

**Note:** as of HomeScript 4.1 the minimum requirement is Python3+ and HomeBridge 1.x.x+

## Examples
`hs.py -s MainLight 0`  | Switch off  
`hs.py -s MainLight 1`  | Switch on  
`hs.py -s MainLight`   | Toggle  
`hs.py -s lifx -hue 140` | RGB Lights Support  (brightness, hue, saturation, temperature)
`hs.py -s desk -b +10` | Increment/Decrement values

## Easy Match
The script doesn't require full names of the accessories.  

**For example**, if your light is called "MainLight", you can run:  
`hs.py -s MainLight 0` or  
`hs.py -s main 0`  
The script will automatically search for matching substrings and set the accessory value

## Group Actions
You can set multiple accessories (of the same type) in a single command:  
`hs.py -s all lights 1`  
`hs.py -s all switches 0`  

**Looking for maintainers: If you are interested in maintaining this project, feel free to reach out.** 

## Setup
  Important: HomeBridge **must** be run in insecure mode for this script to work!

#### Running HomeBridge in Insecure Mode
 - via Command Line
```
homebridge -I
```

 - via Systemd
```
HOMEBRIDGE_OPTS=-U /var/lib/homebridge -I
```

 - via pm2
```
pm2 stop homebridge; pm2 delete homebridge; pm2 start homebridge -- -I
```

## Installation
  - Install the HomeScript API `pip install homescript` or `pip3 install homescript`
  - On your client computer: Download **hs.py** and move it to a convenient location
    - Edit the script to include your homebridge URL, port and authorization key
    - Change permissions `chmod +x /path/to/hs.py` (on linux)

## Usage
Usage: `hs.py [option] [value]`
### Options:
 - -l, --list    : Lists all available HomeKit accessories
  - Usage: `hs.py -l [argument]`
  - Arguments:
    - \<none\> : lists accessory names
    - aid : lists accessory names with AID value
    - iid : lists accessory names with IID value
    - id : lists accessory names with AID and IID
    - type : lists accessory names with type
    - value : lists accessory names current state
 - -g, --get     :  [EasyMatch] gets current value of accessory
   - Usage: `hs.py -g <accessory-name>`
 - -s, --set     :  [EasyMatch] toggles the accessory On or Off, or sets to the specified value
   - Usage: `hs.py -s <accessory-name> [value]`
   - Arguments:
     - \<accessory-name\> : accessory that you want to change
     - -b : adjusts accessory brightness
     - -hue : adjusts accessory hue
     - -sat : adjusts accessory saturation
     - -t : adjusts accessory color temperature
     - [value] : value that you want to set it to. Prefix +/- to inc/dec
 - all     :  Gets or sets value of multiple HomeKit accessories
   - Usage: `hs.py -g all <accessory-type>`
hs.py -s all \<accessory-type\> value
 - -d, --debug   : generates debug log file.
   - Usage: `hs.py -d <command>`
   - Eg: `hs.py -d -s all lights 0`
 - -h, --help    : prints usage info
 - -v, --version : prints HomeScript version

## API
As of v5.1+ HomeScript is now a fully importable API
```python
import homescript

# Initialize with hostname, port and auth code. Debug and sys.argv are optional
hs = homescript.HomeScript(hostname, port, auth, [debug], [sys.argv])

# Select an accessory or group of accessories. Any get/set/print operation requires accessories to be selected first.
hs.selectAccessory('mainlight')
hs.selectGroup('lights')

hs.printSelectedItems()

# Operates on all selected items
hs.setStates(1)
hs.setValues('Brightness',250)
```
| Function | Description |
| ----- | ----------------|
| HomeScript( hostname: str, port: str, auth: str, debug: Boolean, argv: list ) | Constructor to initialize HomeBridge Connection. Debug: Set to `True` if you want to create debug and exception logfile. Default: None. argv: Only required if debug is `True` |
| getAccessories() | Returns raw list of all available accessories on the Bridge |
| selectAccessories( searchString: str ) | Saves matching accessory into selectedAccessories and returns them |
| selectGroup( searchString: str ) | Saves all matching accessories into selectedAccessories and returns them |
| printAccessories() | Prints all available accessories on the Bridge |
| printSelectedItems() | Prints selectedAccessories |
| getSelectedItems() | Returns selectedAccessories |
| setStates(state: Boolean) | Sets `state` as the on/off value of all item(s) in selectedAccessories. If no argument is specified it toggles the state of all selectedAccessories |
| setValues(attribute: str, value: int) | Sets numeric `value` to attribute of the item(s) in selectedAccessories. Attrubute: Brightness/Hue/Saturation/Color Temperature |
| getVersion() | Does what it says on the can... |

## Troubleshooting/Error Reporting/Contributing
The `debug` option helps generate a logfile for troubleshooting and error detection.  
 - If you face an error, open a new issue on this repo prefixed by [Error] describing the error and attach your **both** your debug log and your exception log, along with any other outputs you receive.
 - If you would like to help improve the tool or request features, open an issue prefixed by [Feature Request] describing the functionality.
 - You **must** attach your debug log or else your issue will be closed. A simple debug log can be obtained from `hs.py -d -l`

## PRs and Commit Template
PRs and commits that you make to this repo must include the following:  
- Type: bug-fix or enhancement
- Description: Brief description about what the commit achieves
- Notes: (heads ups/pointers to other developers if necessary)

<hr/>

## To Do
☑️ Color control for RGB and Hue Lights  
⬜️ Control for PositionOpeners, GarageDoorOpener, LockMechanism  
⬜️ WebColors  
⬜️ Increment/Decrement values  
☑️ Querying API interface to return status of devices to `stdout`  
☑️ Automation creation, viewing and monitoring without Home Hub  

<hr/>

## Changelog
### v5.2
 - Added support for Increment/Decrement values

### v5.1.1
 - Fixed import bug

### v5.1
 - Rewritten from the ground up to be object oriented
 - Now features an importable API

### v5.0
- Support for RGB lights! Now lets you control brightness, hue, saturation and color temperature of your lights!
- Added additional value format recognition
- Device type detection
- Updated accessory structure
- Added smart toggle support for integer values
- Added validity checks for integer values
- Ignore bridge in accessory list
- Updated listing format
- Finer control over listing parameters for devices with multiple interfaces
- Updated exclusive value-only listing for easier interfacing in programs
- Cleaned up accessory name recognition
- Backward compatibility with v4.x syntax for all devices

### v4.1
- Update to python 3
- Update to support HomeBridge v1.0+

### v4.0
- Syntax update to be POSIX compliant
- Get option to return item status
- Introducing Automation and scripting support
- Modularity and Third-party HomeScript Apps
- Version logging
- Improved Debugging
Note: Some parts of release withheld until the next minor release

### v3.0.2
- Bug fix: HomeBridge was displayed as "0"

### v3.0.1
- Added debug support

### v3.0
- Added group actions. You can now set values for all matching accessory types

### v2.2
- Added json listing support

### v2.1
- Added type support to identify accessory type
- Updated help doc

### v2.0
- List of accessories are now automatically fetched from the homebridge, instead of having to manually set them up in the script

### v1.3
- Added easy name matching

### v1.2
- Added help doc
- Added listing

### v1.1
- Added toggling

### v1.0
- Initial release

<hr/>
