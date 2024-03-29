import utime
from machine import I2C, Pin

from LiquidCrystal import LiquidCrystal_I2C


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)  # I2C object.
    lcd = LiquidCrystal_I2C(port=i2c)  # LCD object.

    lcd.backlight(status=True)
    lcd.clear_display()
    lcd.set_cursor(0, 0)
    lcd.print("Hello, World!")

    lcd.custom_character(0, (0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F))  # 0% Empty
    lcd.custom_character(1, (0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x1F))  # 16%
    lcd.custom_character(2, (0x0E, 0x1B, 0x11, 0x11, 0x11, 0x1F, 0x1F, 0x1F))  # 33%
    lcd.custom_character(3, (0x0E, 0x1B, 0x11, 0x11, 0x1F, 0x1F, 0x1F, 0x1F))  # 50%
    lcd.custom_character(4, (0x0E, 0x1B, 0x11, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F))  # 66%
    lcd.custom_character(5, (0x0E, 0x1B, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F))  # 83%
    lcd.custom_character(6, (0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F))  # # 100% Full
    lcd.custom_character(7, (0x0E, 0x1F, 0x1B, 0x1B, 0x1B, 0x1F, 0x1B, 0x1F))  # ! Error

    while True:
        lcd.clear_display()
        for i in range(8):
            lcd.set_cursor(0, 0)
            lcd.print(chr(i))
            utime.sleep_ms(150)


if __name__ == "__main__":
    main()
