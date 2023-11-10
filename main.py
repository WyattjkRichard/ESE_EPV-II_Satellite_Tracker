import requests
import json
import geocoder
import ephem
from datetime import datetime

TLE_URL = "https://tle.ivanstanojevic.me/api/tle/25544"


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


if __name__ == '__main__':
    response = requests.get(TLE_URL)
    jprint(response.json())

    TLEName = response.json()['name']
    TLELine1 = response.json()['line1']
    TLELine2 = response.json()['line2']
    sat = ephem.readtle(TLEName, TLELine1, TLELine2)

    satDish = ephem.Observer()
    satDish.lat, satDish.long = geocoder.ip('me').latlng
    satDish.date = datetime.now()

    sat.compute(satDish)

    print(sat.az)
    print(sat.alt)
