import utime
from machine import Pin
from micropython import const

from .instructions import Instruction
from .liquid_crystal_api import HD44780API


class LiquidCrystal(HD44780API):
    __GPIO_LEN: tuple = const((7, 11))  # GPIO list maximum length
    __RS, __RW, __EN = const((0, 1, 2))  # RS, RW and EN Pin mapping

    FONT5X8, FONT5X10 = const((Instruction.FONT5X8, Instruction.FONT5X10))

    def __init__(self, gpio_list: tuple, row: int = 2, col: int = 16, font: int = FONT5X8) -> None:
        """
        Initializes an interface to control an HD44780-compatible LCD using a specified set of GPIO pins.

        :param gpio_list: List of GPIO pins for RS, RW, EN, and (D4 to D7) or (D0 to D7).
        :param row: Number of rows on the LCD (default is 2).
        :param col: Number of columns on the LCD (default is 16).
        :param font: Font size (default is 5x8).
        :raises ValueError: If the length of gpio_list is not equal to 7 or 11.
        """
        super().__init__(row, col)

        if len(gpio_list) not in self.__GPIO_LEN:
            raise ValueError(
                f"Invalid GPIO list! Expected {self.__GPIO_LEN} GPIO pins, but received {len(gpio_list)} pins."
            )

        # predict mode base on len of gpio_list
        self.__data_len: int = (
            Instruction.LEN_8BIT if len(gpio_list) >= 11 else Instruction.LEN_4BIT
        )

        # List of 'Pin' objects, row and font size
        self.__gpio_list: list[Pin] = [Pin(pin, Pin.OUT) for pin in gpio_list]
        self.__num_row = Instruction.LINE2 if row >= 2 else Instruction.LINE1
        self.__font_size: int = font
        self.__init_lcd()  # Initialize the LCD

    def __toggle_enable(self) -> None:
        """
        Toggles the Enable (EN) pin to execute the command.

        :return: None
        """
        self.__gpio_list[self.__EN].value(False)
        utime.sleep_us(40)
        self.__gpio_list[self.__EN].value(True)
        utime.sleep_us(40)
        self.__gpio_list[self.__EN].value(False)

    def __write_gpio(self, write_data: int, mode: int = 8) -> None:
        """
        Writes data to the GPIO pins.

        :param write_data: Data to be written.
        :param mode: Data mode (8 or 4 bits).
        :return: None
        """
        for pin, bit in enumerate(range(mode)):
            self.__gpio_list[3:][pin].value((write_data >> bit) & 0x01)

        # Toggle to enable. To execute previously received data
        self.__toggle_enable()

    def __send_instructions(self, data: int, rs: bool = False) -> None:
        """
        Sends instructions to the LCD.

        :param data: Instruction or data to be sent.
        :param rs: Register Select (True for data, False for instruction).
        :return: None
        """
        self.__gpio_list[self.__RS].value(rs)  # Set RS
        self.__gpio_list[self.__RW].value(False)  # Set RW

        # Handle if 4-bit mode
        if self.__data_len == Instruction.LEN_4BIT:
            msb_data: int = (data >> 4) & 0x0F
            lsb_data: int = data & 0x0F

            self.__write_gpio(msb_data, 4)  # MSB
            self.__write_gpio(lsb_data, 4)  # LSB
            return

        self.__write_gpio(data)  # Write 8-bit mode

    @staticmethod
    def backlight(pin: int, status: bool) -> None:
        """
        Controls the backlight of the LCD.

        :param pin: GPIO pin for backlight control.
        :param status: Backlight status (True for ON, False for OFF).
        :return: None
        """
        if not isinstance(status, bool):
            raise ValueError("The backlight 'status' must be a boolean value (True or False).")

        backlight = Pin(pin, Pin.OUT)  # Backlight object
        backlight.value(status)

    def __init_lcd(self) -> None:
        """
        Initializes the LCD by sending initialization commands.

        :return: None
        """
        # Wait for more than 40 ms after VCC rises to 2.7 V
        utime.sleep_ms(50)
        self.__send_instructions(0x30)  # Function set (Interface is 8 bits long.)
        utime.sleep_ms(5)  # Wait for more than 4.1 ms
        self.__send_instructions(0x30)  # Function set (Interface is 8 bits long.)
        utime.sleep_us(100)  # Wait for more than 100 µs
        self.__send_instructions(0x30)  # Function set (Interface is 8 bits long.)

        # Function set: interface mode, number of lines (rows), and font size
        self.__send_instructions(Instruction.FUNCTION_SET >> 4)
        self.__send_instructions(
            Instruction.FUNCTION_SET | self.__data_len | self.__num_row | self.__font_size
        )

        self.display_on()  # Display control: Display on, cursor and blink off
        self.clear_display()  # Clear display

        # Entry mode set: Increment display, No shift
        self.__send_instructions(Instruction.ENTRY_MODE_SET | Instruction.INCREMENT)


# THE END
