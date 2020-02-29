import json
import csv

def rawdata_to_csv(dataset):
    length = len(dataset['Find']['Result'])
    final_json = []
    for i in range(length):
        final_json.append(flatten_json(dataset['Find']['Result'][i]))

    csv_columns = ['Light_parentDomain', 'Light_deviceState_connState_connected',
                   'Light_deviceState_connState_since',
                   'Light_state_reliability', 'Light_tenantId', 'Light_locationId_2',
                   'Light_geocoordinates_longitude',
                   'Light_lastUpdated', 'Light_sid', 'Light_geohash', 'Light_private_lamp_Status',
                   'Light_state_powerConsumption',
                   'Light_createTime', 'Light_isValid', 'Light_powerMeter', 'Light_locationName_0',
                   'Light_state_intensityLevel_request_value',
                   'Light_applicableDomain_0', 'Light_status', 'Light_state_intensityLevel_lastKnownValue',
                   'Light_locationId_1',
                   'Light_locationId_0', 'Light_mode_0', 'Light_locationId_3', 'Light_thirdPartyId',
                   'Light_providerDetails_provider',
                   'Light_isIndependent', 'Light_label', 'Light_geocoordinates_latitude']

    with open('lighting_data_modified.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in final_json:
            writer.writerow(data)


def flatten_json(nestedjsondata):
    out = {}

    def flatten(x, name = ''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nestedjsondata)
    return out


with open('/home/anand/100-Days-Of-DataEngineering-Code/Day_8_29022020/jsondata.json', 'r') as jsondata:
    jsondict = json.load(jsondata)
    rawdata_to_csv(jsondict)


