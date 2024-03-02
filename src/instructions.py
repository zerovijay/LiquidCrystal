from micropython import const


class Instruction:
    # LiquidCrystal core instructions flags.
    CLEAR_DISPLAY: int = const(0x01)
    RETURN_HOME: int = const(0x02)
    ENTRY_MODE_SET: int = const(0x04)
    DISPLAY_CONTROL: int = const(0x08)
    CRD_SHIFT: int = const(0x10)  # Cursor or display shift.
    FUNCTION_SET: int = const(0x20)
    CGRAM_ADDR: int = const(0x40)
    DDRAM_ADDR: int = const(0x80)

    # Entry mode instructions sub flags.
    INCREMENT: int = const(0x02)
    SHIFT: int = const(0x01)

    # Display on/off instructions sub flags.
    DISPLAY: int = const(0x04)
    CURSOR: int = const(0x02)
    BLINK: int = const(0x01)

    # Display or cursor shift instructions sub flags.
    CURSOR_MOVE: int = const(0x00)
    DISPLAY_SHIFT: int = const(0x08)
    SHIFT_RIGHT: int = const(0x04)
    SHIFT_LEFT: int = const(0x00)

    # Function set instructions sub flags.
    LEN_8BIT: int = const(0x10)
    LEN_4BIT: int = const(0x00)
    LINE1: int = const(0x00)
    LINE2: int = const(0x08)
    FONT5X8: int = const(0x00)
    FONT5X10: int = const(0x04)


# THE END
