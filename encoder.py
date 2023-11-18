ENC_ADDRESS = 0x36

# Register addresses for angle data
ANGLE_REGISTER_HIGH = 0x0E
ANGLE_REGISTER_LOW = 0x0F


def read_angle(bus):
    # Read 14 bits for the angle (high and low registers)
    high_byte = bus.read_byte_data(ENC_ADDRESS, ANGLE_REGISTER_HIGH)
    low_byte = bus.read_byte_data(ENC_ADDRESS, ANGLE_REGISTER_LOW)

    # Combine high and low bytes to get the 14-bit angle value
    angle_raw = (high_byte << 8) | low_byte

    # Convert the raw value to degrees (0-360)
    angle_deg = (angle_raw * 360) / 16384

    return angle_deg
