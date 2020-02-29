import requests
import sys

base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
key  = 'AIzaSyCkYIivaW0dUHggGVsbJypnF_q1mK9JDVQ'

def get_location(tenant):
    attribute = "address="
    url_with_attr = base_url + attribute + tenant.capitalize() + '&key=' + key
    print(url_with_attr)
    r = requests.get(url_with_attr)
    if r.status_code == 200:
        if r.text == "":
            return "nil"
        else:
            return r.json() #['results'][0]['geometry']['bounds']
    else:
        r = dict(results="")
        return r


if __name__ == '__main__':
    tenant = sys.argv[1]
bbox = get_location(tenant)
print(bbox)