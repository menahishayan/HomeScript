# HomeScript
Python script for command line control of [HomeBridge](https://github.com/nfarina/homebridge) (HomeKit)

Used to toggle Homebridge accessories On or Off via python script, no Home app required. You can set up a cronjob to enable automation, scripting and mimic other HomeKit functionalities

## Examples
`homeScript.py MainLight 0`  | Switch off  
`homeScript.py MainLight 1`  | Switch on  
`homeScript.py MainLight`   | Toggle

## Easy Match
The script doesn't require full names of the accessories.  

**For example**, if your light is called "MainLight", you can run:  
`homeScript.py MainLight 0` or  
`homeScript.py main 0`  
The script will automatically search for matching substrings and set the accessory value

## Group Actions
You can set multiple accessories (of the same type) in a single command:  
`homeScript.py all lights 1`  
`homeScript.py all switches 0`  

## Dependencies
 - Python requests library
 - Python JSON library
 
 ## Installation
  - Install the requests library `pip install requests` or `pip3 install requests`
  - On your client computer: Move **homeScript.py** to a convenient location 
    - Edit the script to include your homebridge URL, port and authorization key
    - Change permissions `chmod +x /path/to/homeScript.py` (on linux)
  - On your HomeBridge: edit your **/etc/default/homebridge** to run in insecure mode every time it starts. 
    - `HOMEBRIDGE_OPTS=-I -U /var/lib/homebridge`
    - Restart your homebridge for the changes to take effect: `sudo systemctl restart homebridge.service` or the equivalent command on your device.
    
## Usage
`homeScript.py [option] [argument]`
### Options:
 - list : lists all available HomeKit accessories
   - Usage: `homeScript.py list [argument]`
   - Arguments:
     - \<none\> : lists accessory names
     - aid : lists accessory names with AID value
     - iid : lists accessory names with IID value
     - id : lists accessory names with AID and IID
     - type : lists accessory names with type [Lightbulb, Switch, Fan, etc.]
     - value : lists accessory names current state
     - all : lists all of the above
     - json: prints all attributes in JSON string format
 - \<accessory-name\> : [EasyMatch Supported] toggles the accessory On or Off, or sets to value
   - Usage: `homeScript.py <accessory-name> [value]`
   - Values:
     - \<none\> : toggles the state
     - 0 : sets to OFF
     - 1 : sets to ON
 - all : sets value of multiple HomeKit accessories
   - Usage: `homeScript.py all <accessory-type> value`
   - \<accessory-type\> : [EasyMatch Supported] sets all \<accessory-type\> to \<value\>
 - help : prints usage info
 - debug : generates debug log file.
   - Usage: `homeScript.py debug <command>`
   - Eg: `homeScript.py debug all lights 0`

## Troubleshooting/Error Reporting/Contributing
The `debug` option helps generate a logfile for troubleshooting and error detection.  
 - If you face an error, open a new issue on this repo prefixed by [Error] describing the error and attach your **both** your debug log and your exception log, along with any other outputs you receive.
 - If you would like to help improve the tool or request features, open an issue prefixed by [Feature Request] describing the functionality.
 - You **must** attach your debug log or else your issue will be closed. A simple debug log can be obtained from `homeScript.py debug list`

## PRs and Commit Template
PRs and commits that you make to this repo must include the following:  
- Type: bug-fix or enhancement
- Description: Brief description about what the commit achieves
- Notes: (heads ups/pointers to other developers if necessary)

<hr/>

## To Do
⬜️ Color control for RGB and Hue Lights  
⬜️ Control for PositionOpeners, GarageDoorOpener, LockMechanism  
⬜️ Querying API interface to return status of devices to `stdout`  
⬜️ Automation creation, viewing and monitoring without Home Hub  

<hr/>

## Changelog
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

