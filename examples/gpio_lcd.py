import utime

from LiquidCrystal import LiquidCrystal


def main() -> None:
    gpio_list: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 8bit mode
    # gpio_list: list[int] = [2, 3, 4, 9, 10, 11, 12] # 4bit mode

    # Initialize LCD with default parameters (2 rows, 16 columns, 5x8 font)
    lcd = LiquidCrystal(gpio_list)

    lcd.backlight(13, True)  # Backlight on, at GPIO 13
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
