def get_temperature(hs):
    hs_print_output = hs.getSelectedItems()
    for item in hs_print_output:
        if item["value"][0]["description"] == 'Current Temperature':
            temperature = item["value"][0]["value"]
            return temperature # °C
    print("Temperature Sensor Not Found!")

def get_humidity(hs):
    hs_print_output = hs.getSelectedItems()
    for item in hs_print_output:
        if item["value"][0]["description"] == 'Current Relative Humidity':
            humidity = item["value"][0]["value"]
            return humidity # %
    print("Humidity Sensor Not Found!")