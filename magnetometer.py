MAGNETOMETER_ADDRESS = 0x1E     # D0 must be tied high to 3.3v

# Register addresses
WHO_AM_I = 0x0F         # Device identification register.
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22
CTRL_REG4 = 0x23
CTRL_REG5 = 0x24
STATUS_REG = 0x27
OUT_X_L = 0x28          # X-axis data output. The value of magnetic field is expressed as two’s complement.
OUT_X_H = 0x29          # X-axis data output. The value of magnetic field is expressed as two’s complement.
OUT_Y_L = 0x2A          # Y-axis data output. The value of magnetic field is expressed as two’s complement.
OUT_Y_H = 0x2B          # Y-axis data output. The value of magnetic field is expressed as two’s complement.
OUT_Z_L = 0x2C          # Z-axis data output. The value of magnetic field is expressed as two’s complement.
OUT_Z_H = 0x2D          # Z-axis data output. The value of magnetic field is expressed as two’s complement.
TEMP_OUT_L = 0x2E       # Temperature sensor data. The value of temperature is expressed as two’s complement.
TEMP_OUT_H = 0x2F       # Temperature sensor data. The value of temperature is expressed as two’s complement.
INT_CFG = 0x30          # Interrupt configuration register
INT_SRC = 0x31          # Interrupt source register
INT_THS_L = 0x32        # Interrupt threshold.
INT_THS_H = 0x33        # Interrupt threshold.


def read_heading(bus):

    bus.write_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG2, 0b00001000)
    # Read magnetometer data registers
    mag_x_low = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_X_L)
    mag_x_high = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_X_H)
    mag_y_low = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_Y_L)
    mag_y_high = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_Y_H)
    mag_z_low = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_Z_L)
    mag_z_high = bus.read_byte_data(MAGNETOMETER_ADDRESS, OUT_Z_H)

    # Combine low and high bytes for each axis
    mag_x = (mag_x_high << 8) | mag_x_low
    mag_y = (mag_y_high << 8) | mag_y_low
    mag_z = (mag_z_high << 8) | mag_z_low

    return mag_x, mag_y, mag_z

def read_ctl(bus):
    ctl1 = format(bus.read_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG1), '#010b')
    ctl2 = format(bus.read_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG2), '#010b')
    ctl3 = format(bus.read_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG3), '#010b')
    ctl4 = format(bus.read_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG4), '#010b')
    ctl5 = format(bus.read_byte_data(MAGNETOMETER_ADDRESS, CTRL_REG5), '#010b')
    return ctl1, ctl2, ctl3, ctl4, ctl5
