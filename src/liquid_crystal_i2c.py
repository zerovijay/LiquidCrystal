import utime
from machine import I2C
from micropython import const

from .PCF8574T import PCF8574T
from .instructions import Instruction
from .liquid_crystal_api import HD44780API


class LiquidCrystal_I2C(HD44780API):
    # Pin mapping for RS, RW, EN, and BACKLIGHT.
    __RS, __RW, __EN, __BL = const((0, 1, 2, 3))

    # Macro for Font size.
    FONT5X8, FONT5X10 = const((Instruction.FONT5X8, Instruction.FONT5X10))

    def __init__(self, port: I2C, addr: int = 0x27, row: int = 2, col: int = 16, font: int = FONT5X8) -> None:
        """
        Initialize the I2C-based LCD object.

        :param port: I2C port for communication.
        :param addr: I2C address of the LCD.
        :param row: Number of rows on the LCD (default is 2).
        :param col: Number of columns on the LCD (default is 16).
        :param font: Font size (default is 5x8).
        :raises TypeError: If the provided port is not a valid I2C object.
        """
        super().__init__(row, col)
        self.__io_exp = PCF8574T(port, addr)  # GPIO Expander object.

        # Set GPIO pins as output
        for pin in range(self.__io_exp.PIN_MIN, self.__io_exp.PIN_MAX):
            self.__io_exp.pin_mode(pin, self.__io_exp.OUTPUT)

        self.__num_row = Instruction.LINE2 if row >= 2 else Instruction.LINE1
        self.__font_size: int = font
        self.__init_lcd()  # Initialize the LCD.

    def __toggle_enable(self) -> None:
        """
        Toggle the Enable (EN) pin to execute the command.

        :return: None
        """
        self.__io_exp.digital_write(self.__EN, True)
        utime.sleep_us(40)
        self.__io_exp.digital_write(self.__EN, False)

    def __write_nibble(self, nibble: int) -> None:
        """
        Write a 4-bit nibble to the GPIO expander.

        :param nibble: The 4-bit nibble to be written.
        :return: None
        """
        for pin, bit in enumerate(range(4), start=4):
            self.__io_exp.digital_write(pin, (nibble >> bit) & 0x01)

        # Toggle to enable. To execute previously received data.
        self.__toggle_enable()

    def __send_instructions(self, data: int, rs: bool = False) -> None:
        """
        Send instructions to the LCD.

        :param data: Instruction or data to be sent.
        :param rs: Register Select (True for data, False for instruction).
        :return: None
        """
        msb_data: int = (data >> 4) & 0x0F
        lsb_data: int = data & 0x0F

        # Set RS and RW signals.
        self.__io_exp.digital_write(self.__RS, rs)
        self.__io_exp.digital_write(self.__RW, False)  # RW: 0 (Write mode).

        # Send high nibble (MSB) first, followed by low nibble (LSB).
        self.__write_nibble(msb_data)
        self.__write_nibble(lsb_data)

    def backlight(self, status: bool = False) -> None:
        """
        Control the backlight of the LCD.

        :param status: Backlight status (True for ON, False for OFF).
        :return: None
        """
        if not isinstance(status, bool):
            raise ValueError("Backlight 'status' must be a boolean (True or False).")

        # Set the 3rd pin 'PB3' for the LCD backlight.
        self.__io_exp.digital_write(self.__BL, status)

    def __init_lcd(self) -> None:
        """
        Initialize the LCD by sending initialization commands.

        :return: None
        """
        # Wait for more than 40 ms after VCC rises to 2.7 V.
        utime.sleep_ms(50)
        self.__send_instructions(0x03)  # Function set (Interface is 8 bits long.)
        utime.sleep_ms(5)  # Wait for more than 4.1 ms.
        self.__send_instructions(0x03)  # Function set (Interface is 8 bits long.)
        utime.sleep_us(100)  # Wait for more than 100 µs.
        self.__send_instructions(0x03)  # Function set (Interface is 8 bits long.)

        # Function set: 4-bit mode, display lines, font size.
        self.__send_instructions(Instruction.FUNCTION_SET >> 4)
        self.__send_instructions(Instruction.FUNCTION_SET | Instruction.LEN_4BIT | self.__num_row | self.__font_size)

        self.display_on()  # Display control: Display on, cursor and blink off.
        self.clear_display()  # Clear display.

        # Entry mode set: Increment display, No shift.
        self.__send_instructions(Instruction.ENTRY_MODE_SET | Instruction.INCREMENT)


# THE END
