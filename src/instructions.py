from micropython import const


# LiquidCrystal instructions flags.
class Instruction:
    CLEAR_DISPLAY: int = const(0x01)
    RETURN_HOME: int = const(0x02)

    ENTRY_MODE_SET: int = const(0x04)
    INCREMENT: int = const(0x02)
    SHIFT: int = const(0x01)

    DISPLAY_CONTROL: int = const(0x08)
    DISPLAY: int = const(0x04)
    CURSOR: int = const(0x02)
    BLINK: int = const(0x01)

    CRD_SHIFT: int = const(0x10)  # Cursor or display shift.
    CURSOR_MOVE: int = const(0x00)
    DISPLAY_SHIFT: int = const(0x08)
    SHIFT_RIGHT: int = const(0x04)
    SHIFT_LEFT: int = const(0x00)

    FUNCTION_SET: int = const(0x20)
    LEN_8BIT: int = const(0x10)
    LEN_4BIT: int = const(0x00)
    DISPLAY_1LINE: int = const(0x00)
    DISPLAY_2LINE: int = const(0x08)
    FONT5X8: int = const(0x00)
    FONT5X10: int = const(0x04)

    CGRAM_ADDR: int = const(0x40)
    DDRAM_ADDR: int = const(0x80)


# THE END
