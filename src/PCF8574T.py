import ustruct
from machine import I2C
from micropython import const


class PCF8574T:
    # Constants (MACRO) representing pin modes and pin range.
    DEFAULT_ADDR: int = const(0x20)
    PIN_MIN, PIN_MAX = const((0, 7))
    INPUT, INPUT_PULLUP, OUTPUT, OUTPUT_PULLUP = const((1, 1, 0, 1))  # Pin modes.

    def __init__(self, port: I2C, addr: int = DEFAULT_ADDR) -> None:
        """
        Initialize the PCF8574 instance.

        :param port: An I2C object representing the communication bus.
        :param addr: The I2C address of the PCF8574 device.
        :raises ValueError: If the provided address is not valid.
        :raises TypeError: If the provided port is not a valid I2C object.
        """
        # Check if the provided address is within the valid range for PCF8574.
        if not (0x20 <= addr <= 0x27 or 0x38 <= addr <= 0x3F):
            raise ValueError(f"Invalid device address: {hex(addr)}")

        # Ensure that the provided port is a valid I2C object.
        if not isinstance(port, I2C):
            raise TypeError("Invalid I2C object! Please provide a valid I2C object.")

        # Initialize instance variables.
        self.__i2c_device: I2C = port  # I2C object.
        self.__io_exp_addr: int = const(addr)  # Device address.
        self.__io_write: int = 0x00  # Write buffer.
        self.__io_config: int = 0x00  # Configuration buffer.

        # Check if the device is present on the I2C bus.
        if self.__io_exp_addr not in self.__i2c_device.scan():
            raise OSError("Device not found on the I2C bus!")

    def __expander_read(self, fmt: str = ">B") -> int:
        """
        Read the current state of all pins from the I/O expander.

        :return: The status byte represents the state of all pins.
        :raises RuntimeError: If there is an error during the read operation.
        """
        try:
            data: bytes = self.__i2c_device.readfrom(self.__io_exp_addr, 1)
            return ustruct.unpack(fmt, data)[0]  # Interpret the byte as an unsigned integer.
        except OSError as read_error:
            raise RuntimeError(f"Expander read error: {read_error}")

    def __expander_write(self, data: int) -> None:
        """
        Writes data to the I/O expander.

        :param data: The data to be written to the I/O expander.
        :raises RuntimeError: If the expander fails to write.
        """
        try:
            self.__i2c_device.writeto(self.__io_exp_addr, bytes([data]))
        except OSError as write_error:
            raise RuntimeError(f"Expander write error: {write_error}")

    def read_byte(self) -> int:
        """
        Read the current state of all pins from the I/O expander.

        :return: The status byte represents the state of all pins.
        :raises RuntimeError: If there is an error during the read operation.
        """
        return self.__expander_read()

    def write_byte(self, byte: int) -> None:
        """
        Write data to the I/O expander.

        :param byte: The byte to be written to the I/O expander.
        :raises RuntimeError: If the expander fails to write.
        """
        self.__expander_write(byte)

    def pin_mode(self, pin_num: int, mode: int) -> None:
        """
        Set the mode (INPUT or OUTPUT) for a specific pin.

        :param pin_num: The pin to configure.
        :param mode: The mode to set (INPUT or OUTPUT).
        :raises ValueError: If the provided pin is not within the valid range.
        """
        if not self.PIN_MIN <= pin_num <= self.PIN_MAX:
            raise ValueError(f"Invalid pin number: {pin_num}")

        if mode not in (self.INPUT, self.INPUT_PULLUP, self.OUTPUT, self.OUTPUT_PULLUP):
            raise ValueError(f"Invalid pin mode to configure the pin {pin_num}")

        # Set or clear the corresponding bit in the io configuration buffer based on the specified mode.
        self.__io_write = (self.__io_write & ~(1 << pin_num)) | (mode << pin_num)
        self.__expander_write(self.__io_config)  # Update the configuration buffer.

    def digital_write(self, pin_num: int, value: int) -> None:
        """
        Write a digital value (0 or 1) to a specific pin.

        :param pin_num: The pin to write to.
        :param value: The value to write (0 or 1).
        :raises ValueError: If the provided pin is not within the valid range.
        :raises ValueError: If the pin is not configured as an output.
        """
        if not self.PIN_MIN <= pin_num <= self.PIN_MAX:
            raise ValueError(f"Invalid pin number: {pin_num}")

        # Set or clear the corresponding bit in the write buffer based on the specified value.
        self.__io_write = (self.__io_write & ~(1 << pin_num)) | (value << pin_num)
        self.__expander_write(self.__io_write)  # Update the write buffer.

    def digital_read(self, pin_num: int) -> int:
        """
        Read the digital value (0 or 1) from a specific input pin.

        :param pin_num: The pin to read from (0 to 7).
        :return: The digital value (0 or 1) read from the specified pin.
        :raises ValueError: If the provided pin is not within the valid range.
        :raises ValueError: If the pin is not configured as an input.
        :raises RuntimeError: If there is an error during the read operation.
        """
        if not self.PIN_MIN <= pin_num <= self.PIN_MAX:
            raise ValueError(f"Invalid pin number: {pin_num}")

        status: int = self.__expander_read()  # Read the GPIO status.
        return (status >> pin_num) & 0x01  # Extract a bit from the byte for the pin.

    def __del__(self) -> None:
        """
        Clean up and deinitialize the I2C interface.

        This method should be called when you are done using the object,
        to ensure proper resource cleanup.

        :return: None
        """
        self.__i2c_device.deinit()


# THE END
