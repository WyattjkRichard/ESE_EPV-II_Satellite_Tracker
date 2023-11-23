from smbus2 import i2c_msg

# setup limit switches
MOTOR_ADDRESS = 0x0F     # D0 must be tied high to 3.3v


class TicI2C(object):
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def motor_init_limit_switch(self):
        self.bus.write_byte_data(MOTOR_ADDRESS, 0x3D, 0x08)  # init limit switch forward
        self.bus.write_byte_data(MOTOR_ADDRESS, 0x3E, 0x09)  # init limit switch reverse

    def energize(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x85])
        self.bus.i2c_rdwr(msg)

    def de_energize(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x86])
        self.bus.i2c_rdwr(msg)

    # Reset command timeout
    def rst_cmd_to(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x8C])
        self.bus.i2c_rdwr(msg)

    def exit_safe_start(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x8F])
        self.bus.i2c_rdwr(msg)

    def home_forward(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x97, 0x01])
        self.bus.i2c_rdwr(msg)

    def home_reverse(self):
        msg = i2c_msg.write(MOTOR_ADDRESS, [0x97, 0x00])
        self.bus.i2c_rdwr(msg)

    def set_target_position(self, target):
        command = [0xE0,
                   target >> 0 & 0xFF,
                   target >> 8 & 0xFF,
                   target >> 16 & 0xFF,
                   target >> 24 & 0xFF]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

        # Gets one or more variables from the Tic.

    def get_current_position(self):
        b = self.get_variables(0x22, 4)
        position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
        if position >= (1 << 31):
            position -= (1 << 32)
        return position

    # Gets one or more variables from the Tic.
    def get_variables(self, offset, length):
        write = i2c_msg.write(self.address, [0xA1, offset])
        read = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(write, read)
        return list(read)
