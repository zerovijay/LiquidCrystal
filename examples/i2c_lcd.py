import utime
from machine import I2C, Pin

from LiquidCrystal import LiquidCrystal_I2C


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

    # Initialize LCD with default parameters (2 rows, 16 columns, 5x8 font)
    lcd = LiquidCrystal_I2C(i2c)

    lcd.backlight(True)  # Backlight on
    lcd.clear_display()
    lcd.set_cursor(0, 0)  # Set the cursor to print
    lcd.print("Hello, World!")

    while True:
        for i in range(100):
            lcd.set_cursor(1, 0)  # allocate space for print variable
            lcd.print("       ")  # Fill some space for avoid display clear
            lcd.set_cursor(1, 0)
            lcd.print(i)  # Print the variable
            utime.sleep_ms(500)


if __name__ == "__main__":
    main()
