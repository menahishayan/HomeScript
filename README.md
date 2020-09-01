# HomeScript
Python script for command line control of [HomeBridge](https://github.com/nfarina/homebridge) (HomeKit)

Used to toggle Homebridge accessories On or Off via python script, no Home app required. You can set up a cronjob to enable automation, scripting and mimic other HomeKit functionalities

**Note:** as of HomeScript 4.1 the minimum requirement is Python3+ and HomeBridge 1.x.x+

## Examples
`homeScript.py -s MainLight 0`  | Switch off  
`homeScript.py -s MainLight 1`  | Switch on  
`homeScript.py -s MainLight`   | Toggle  
`homeScript.py -s lifx --hue 140` | RGB Lights Support  
`homeScript.py -s lifx --saturation` | Toggle even works on integer values

## Easy Match
The script doesn't require full names of the accessories.  

**For example**, if your light is called "MainLight", you can run:  
`homeScript.py -s MainLight 0` or  
`homeScript.py -s main 0`  
The script will automatically search for matching substrings and set the accessory value

## Group Actions
You can set multiple accessories (of the same type) in a single command:  
`homeScript.py -s all lights 1`  
`homeScript.py -s all switches 0`  

## Automations
HomeScript allows you to create automations **without** a Home Hub!  
Read: [AUTOMATION.md](AUTOMATION.md)

## HS Apps
Introducing HomeScript Apps! Allows for modularity and extendability using custom third-party apps and scripts. WIP

**Looking for maintainers: This repo is no longer being maintained and future updates to this project may not be guaranteed. If you are interested in maintaining this project, feel free to reach out.** 

## Dependencies
 - Python requests library
 - Python JSON library

 ## Installation
  - Install the requests library `pip install requests` or `pip3 install requests`
  - On your client computer: Move **homeScript.py** to a convenient location
    - Edit the script to include your homebridge URL, port and authorization key
    - Change permissions `chmod +x /path/to/homeScript.py` (on linux)

## Usage
Usage: `homeScript.py [option] [value]`
### Options:
 - -l, --list    : Lists all available HomeKit accessories
  - Usage: `homeScript.py -l [argument]`
  - Arguments:
    - \<none\> : lists accessory names
    - aid : lists accessory names with AID value
    - iid : lists accessory names with IID value
    - id : lists accessory names with AID and IID
    - type : lists accessory names with type
    - value : lists accessory names current state
 - -g, --get     :  [EasyMatch] gets current value of accessory
   - Usage: `homeScript.py -g <accessory-name>`
 - -s, --set     :  [EasyMatch] toggles the accessory On or Off, or sets to the specified value
   - Usage: `homeScript.py -s <accessory-name> [value]`
   - Arguments:
     - \<accessory-name\> : accessory that you want to change
     - -b, --brightness : adjusts accessory brightness
     - -h, --hue : adjusts accessory hue
     - -sat, --saturation : adjusts accessory saturation
     - -t, --temperature : adjusts accessory color temperature
     - [value] : value that you want to set it to
 - all     :  Gets or sets value of multiple HomeKit accessories
   - Usage: `homeScript.py -g all <accessory-type>`
homeScript.py -s all <accessory-type> value
 - -d, --debug   : generates debug log file.
   - Usage: `homeScript.py -d <command>`
   - Eg: `homeScript.py -d -s all lights 0`
 - -h, --help    : prints usage info
 - -v, --version : prints HomeScript version


## Troubleshooting/Error Reporting/Contributing
The `debug` option helps generate a logfile for troubleshooting and error detection.  
 - If you face an error, open a new issue on this repo prefixed by [Error] describing the error and attach your **both** your debug log and your exception log, along with any other outputs you receive.
 - If you would like to help improve the tool or request features, open an issue prefixed by [Feature Request] describing the functionality.
 - You **must** attach your debug log or else your issue will be closed. A simple debug log can be obtained from `homeScript.py -d -l`

## PRs and Commit Template
PRs and commits that you make to this repo must include the following:  
- Type: bug-fix or enhancement
- Description: Brief description about what the commit achieves
- Notes: (heads ups/pointers to other developers if necessary)

<hr/>

## To Do
☑️ Color control for RGB and Hue Lights  
⬜️ Control for PositionOpeners, GarageDoorOpener, LockMechanism  
☑️ Querying API interface to return status of devices to `stdout`  
☑️ Automation creation, viewing and monitoring without Home Hub  

<hr/>

## Changelog
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
