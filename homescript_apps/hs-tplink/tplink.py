""" Reads the temperature and humidity from a Xiaomi Aqara Temperature and Humidity Sensor
    through a Aqara Air Conditioning Companion Gateway.
"""

def get_state(hs):
    """ Reads the state of the realy from a TP-Link Smart Plug. 

    Parameters
    ----------
    hs : HomeScript
         HomeBridge Connection.
    """
    hs_print_output = hs.getSelectedItems()
    for item in hs_print_output:
        #print(item)
        #print(item["value"])
        #print(item["value"][0])
        #print(item["value"][0]["description"])
        if item["value"][0]["description"] == 'On':
            state = item["value"][0]["value"]
            return state 
    print("Smart Plug Sensor Not Found!")