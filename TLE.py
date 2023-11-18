import geocoder
import ephem
import requests

TLE_URL = "https://tle.ivanstanojevic.me/api/tle/"
ELEV_URL = "https://api.open-elevation.com/api/v1/lookup?locations="

# example TLE data
# "name":"ISS (ZARYA)"
# "line1":"1 25544U 98067A   23314.24517226  .00093162  00000+0  16505-2 0  9991"
# "line2":"2 25544  51.6416 325.0671 0002415 274.2971 187.0056 15.49490004424444"


def init_observer(sat_id):
    response = requests.get(f"{TLE_URL}{sat_id}")
    # ideally, check response to ensure no issues
    tle_name = response.json()['name']
    tle_line1 = response.json()['line1']
    tle_line2 = response.json()['line2']
    satellite = ephem.readtle(tle_name, tle_line1, tle_line2)
    sat_dish = ephem.Observer()
    sat_dish.lat, sat_dish.long = geocoder.ip('me').latlng
    elevation = requests.get(f"{ELEV_URL}{geocoder.ip('me').latlng[0]},{geocoder.ip('me').latlng[1]}").json()["results"][0]["elevation"]
    # print(f"Elevation: {elevation}")
    return sat_dish, satellite
