import json
import time
import smbus2
import RPi.GPIO as GPIO
from datetime import datetime

from TLE import *
from encoder import *
from magnetometer import *

SAT_ID = 25544

# Create I2C bus
bus = smbus2.SMBus(1)  # Use 1 for the Raspberry Pi 3


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


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
    pin = 11
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

    try:
        while True:
            mag_x, mag_y, mag_z = read_heading(bus)
            print(f"Magnetometer Data - X: {mag_x}, Y: {mag_y}, Z: {mag_z}")

            # GPIO.output(pin, 0)
            # angle = read_angle(bus)
            # print(f"Alt angle: {angle:.2f} degrees")

            # GPIO.output(pin, 1)
            # angle2 = read_angle(bus)
            # print(f"Az angle: {angle2:.2f} degrees")

            satDish.date = datetime.utcnow()
            sat.compute(satDish)
            print(f"az: {sat.az}, alt: {sat.alt}\n")

            time.sleep(1)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nExiting program.")
    finally:
        # Cleanup resources
        GPIO.cleanup()
        bus.close()
