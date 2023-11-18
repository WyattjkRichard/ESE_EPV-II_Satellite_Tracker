import requests
import json
import geocoder
import ephem
import time
import smbus
import RPi.GPIO as GPIO
from datetime import datetime

from encoder import read_angle
from magnetometer import read_heading

TLE_URL = "https://tle.ivanstanojevic.me/api/tle/"
ELEV_URL = "https://api.open-elevation.com/api/v1/lookup?locations="

SAT_ID = 25544


# Create I2C bus
bus = smbus.SMBus(1)  # Use 1 for the Raspberry Pi 3

# "name":"ISS (ZARYA)"
# "line1":"1 25544U 98067A   23314.24517226  .00093162  00000+0  16505-2 0  9991"
# "line2":"2 25544  51.6416 325.0671 0002415 274.2971 187.0056 15.49490004424444"


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


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


def gpio_test():
    GPIO.setmode(GPIO.BOARD)
    control_pins = [7, 11, 13, 15]
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    halfstep_seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]
    for i in range(512):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.001)
    GPIO.cleanup()


if __name__ == '__main__':
    satDish, sat = init_observer(SAT_ID)
    # Azimuth: 0-360 deg east of north
    # Altitude: +- 90 deg relative to the horizon's great circle

    satDish.date = datetime.utcnow()
    sat.compute(satDish)
    print(f"az: {sat.az}, alt: {sat.alt}\n")


    try:
        while True:
            mag_x, mag_y, mag_z = read_heading(bus)
            print(f"Magnetometer Data - X: {mag_x}, Y: {mag_y}, Z: {mag_z}")

            angle = read_angle(bus)
            print(f"Angle: {angle:.2f} degrees")

            time.sleep(1)


    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nExiting program.")
    finally:
        # Cleanup resources
        bus.close()
