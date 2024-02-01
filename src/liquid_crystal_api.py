import utime
from micropython import const

from .instructions import Instruction


class HD44780API:
    __ROWS: tuple = const((1, 2, 4))
    __COLUMNS: tuple = const((16, 20))
    __RAM_MIN, __RAM_MAX = const((0, 7))  # Range of valid CGRAM locations

    def __init__(self, row: int, col: int) -> None:
        """
        Initialize the HD44780API object.

        :param row: Number of rows on the display (1, 2, or 4).
        :param col: Number of columns on the display (16 or 20).
        :raises ValueError: If row or col is invalid.
        """
        if row not in self.__ROWS:
            raise ValueError("Invalid row! 'row' must be 1, 2, or 4.")

        if col not in self.__COLUMNS:
            raise ValueError("Invalid col! 'col' must be 16 or 20.")

        self._row: int = row
        self._col: int = col
        self.__num_row = Instruction.LINE2 if row >= 2 else Instruction.LINE1

    def __send_instructions(self, data: int, rs: bool = False) -> None:
        """
        Placeholder method for sending instructions to the LCD.

        This method must be implemented by subclasses to define the actual
        logic for sending instructions to the HD44780 controller.

        :param data: The data/command to be sent.
        :param rs: Control signal for Register Select (RS). False for command, True for data.
        :return: None
        """
        pass

    def clear_display(self) -> None:
        """
        Clears the entire display.

        :return: None
        """
        self.__send_instructions(Instruction.CLEAR_DISPLAY)
        utime.sleep_ms(2)

    def return_home(self) -> None:
        """
        Sets the cursor to the home position.

        :return: None
        """
        self.__send_instructions(Instruction.RETURN_HOME)
        utime.sleep_ms(2)

    def display_on(self) -> None:
        """
        Turns on the display.

        :return: None
        """
        self.__send_instructions(Instruction.DISPLAY_CONTROL | Instruction.DISPLAY)

    def display_off(self) -> None:
        """
        Turns off the display.

        :return: None
        """
        self.__send_instructions(Instruction.DISPLAY_CONTROL)

    def display_cursor(self) -> None:
        """
        Shows the cursor on the display.

        :return: None
        """
        self.__send_instructions(
            Instruction.DISPLAY_CONTROL | Instruction.DISPLAY | Instruction.CURSOR
        )

    def display_no_cursor(self) -> None:
        """
        Hides the cursor on the display.

        :return: None
        """
        self.__send_instructions(Instruction.DISPLAY_CONTROL | Instruction.DISPLAY)

    def cursor_blink(self) -> None:
        """
        Enables blinking cursor.

        :return: None
        """
        self.__send_instructions(
            Instruction.DISPLAY_CONTROL
            | Instruction.DISPLAY
            | Instruction.CURSOR
            | Instruction.BLINK
        )

    def cursor_no_blink(self) -> None:
        """
        Disables blinking cursor.

        :return: None
        """
        self.__send_instructions(
            Instruction.DISPLAY_CONTROL | Instruction.DISPLAY | Instruction.CURSOR
        )

    def display_shift_left(self) -> None:
        """
        Shifts the entire display to the left.

        :return: None
        """
        self.__send_instructions(
            Instruction.CRD_SHIFT | Instruction.DISPLAY_SHIFT | Instruction.SHIFT_LEFT
        )

    def display_shift_right(self) -> None:
        """
        Shifts the entire display to the right.

        :return: None
        """
        self.__send_instructions(
            Instruction.CRD_SHIFT | Instruction.DISPLAY_SHIFT | Instruction.SHIFT_RIGHT
        )

    def cursor_shift_left(self) -> None:
        """
        Shifts the cursor position to the left.

        :return: None
        """
        self.__send_instructions(
            Instruction.CRD_SHIFT | Instruction.CURSOR_MOVE | Instruction.SHIFT_LEFT
        )

    def cursor_shift_right(self) -> None:
        """
        Shifts the cursor position to the right.

        :return: None
        """
        self.__send_instructions(
            Instruction.CRD_SHIFT | Instruction.CURSOR_MOVE | Instruction.SHIFT_RIGHT
        )

    def set_cursor(self, row: int, col: int) -> None:
        """
        Sets the cursor to the specified row and column.

        :param row: The row number (0-indexed).
        :param col: The column number (0-indexed).
        :raises IndexError: If invalid, row or column values are provided.
        :return: None
        """
        if self.__num_row == Instruction.LINE1 and row != 0:
            raise IndexError("Invalid row! Single-line display only supports row 0.")

        if not (0 <= row < self._row):
            raise IndexError(f"Invalid row! 'row' must be in the range 0 to {self._row - 1}.")

        if not (0 <= col < self._col):
            raise IndexError(f"Invalid column! 'col' must be in the range 0 to {self._col - 1}.")

        row_offset: tuple = const((0x00, 0x40, 0x14, 0x54))
        self.__send_instructions(Instruction.DDRAM_ADDR | (row_offset[row] + col))

    def print(self, data: any) -> None:
        """
        Prints the given data on the LCD.

        :param data: The data to be printed (int, float, or str).
        :return: None
        """
        for char in str(data):
            self.__send_instructions(ord(char), rs=True)  # RS: 1 -> Sending data

    def custom_character(self, ram_addr: int, bit_map: list[int] = None) -> None:
        """
        Defines a custom character at the specified CGRAM address with the given bit map.

        :param ram_addr: The CGRAM address (0 to 7) where the character will be stored.
        :param bit_map: The bit map representing the custom character (optional).
        :raises IndexError: If invalid, CGRAM address or bit map values are provided.
        :return: None
        """
        # Check if ram_addr is within the valid range
        if not self.__RAM_MIN <= ram_addr <= self.__RAM_MAX:
            raise IndexError("Invalid ram address! ram address must be in the range of 0 to 7.")

        # Mask ram_addr to ensure it's within the 7 available ram locations
        ram_addr &= 0x07  # We have only 7 ram locations to store.

        # Handle the case where bit_map is not provided
        if bit_map is None:
            # Access the stored character from the CGRAM address.
            self.__send_instructions(ram_addr, rs=True)  # RS: 1 -> Sending data
            return

        # Check if the length of bit_map is within the valid range
        if not 0 <= len(bit_map) <= 8:
            raise IndexError(f"Invalid bit_map length! It must be in the range of 0 to 8.")

        # Find the indices of elements in bit_map that are not integers
        invalid_indices: list = [i for i, bit in enumerate(bit_map) if not isinstance(bit, int)]

        # If there are invalid indices, raise an error with details about the mismatches
        if invalid_indices:
            invalid_values: list = [bit_map[i] for i in invalid_indices]
            raise ValueError(
                f"Invalid bit_map! Elements at indices {invalid_indices} have non-integer values: {invalid_values}."
            )

        # Set the CGRAM address using the provided ram_addr
        self.__send_instructions(Instruction.CGRAM_ADDR | (ram_addr << 3))

        # Load the bit map into the CGRAM
        for bit in bit_map:
            self.__send_instructions(bit, rs=True)  # RS: 1 -> Sending data


# THE END
