# LiquidCrystal MicroPython Library

[![GitHub License](https://img.shields.io/github/license/zerovijay/LiquidCrystal?style=social)](LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/zerovijay/LiquidCrystal?style=social)](https://github.com/zerovijay/LiquidCrystal/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zerovijay/LiquidCrystal?style=social)](https://github.com/zerovijay/LiquidCrystal/forks)
[![GitHub issues](https://img.shields.io/github/issues-raw/zerovijay/LiquidCrystal?style=social)](https://github.com/zerovijay/LiquidCrystal/issues)
[![GitHub Release](https://img.shields.io/github/v/release/zerovijay/LiquidCrystal?style=social)](https://github.com/zerovijay/LiquidCrystal/releases)

## Overview

The LiquidCrystal MicroPython Library simplifies the control of HD44780-compatible LCDs, particularly those connected
via I2C GPIO expanders like PCF8574 and native GPIO communication. Ideal for projects with limited pins, it supports
LCDs with 1, 2, or 4 rows and 16 or 20 columns, providing flexibility. Font customization allows you to choose between
5x8 or 5x10 sizes.

## Features

- **Versatile Display Support:**
    - Compatible with LCDs featuring 1, 2, or 4 rows.
    - Supports LCDs with 16 or 20 columns.

- **Font Customization:**
    - Choose between 5x8 or 5x10 font size for flexible display options.

- **Backlight Control:**
    - Convenient functionality to control the LCD backlight.

- **Display and Cursor Control:**
    - Turn on/off the display.
    - Show/hide the cursor on the display.
    - Enable/disable cursor blinking.

- **Shift Functionality:**
    - Shift the entire display or cursor to the left or right.

- **Clear Display and Home Position:**
    - Clear the entire display.
    - Set the cursor to the home position.

- **Custom Character Support:**
    - Define and display custom characters at specified CGRAM addresses.

- **Simulation:**
    - WOKWI simulation support.

## Installation

Clone the repository:

```bash
git clone https://github.com/zerovijay/LiquidCrystal.git
cd LiquidCrystal 
git submodule init
git submodule update
```

## Getting Started

### Initialization - GPIO-based LCD

```python
from LiquidCrystal import LiquidCrystal

# Example GPIO pin configuration (8-bit mode)
gpio_list = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# Initialize GPIO-based LCD
lcd = LiquidCrystal(gpio_list)

# Display some text with backlight on
lcd.backlight(pin=13, status=True)
lcd.print("Hello, World!")
```

### Initialization - I2C-based LCD

```python
from machine import I2C, Pin
from LiquidCrystal import LiquidCrystal_I2C

# Example I2C configuration
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Initialize I2C-based LCD
lcd = LiquidCrystal_I2C(i2c)

# Display some text with backlight on
lcd.backlight(status=True)
lcd.print("Hello, World!")
```

### Example Usage

```python
import utime
from machine import I2C, Pin
from LiquidCrystal import LiquidCrystal_I2C


def main():
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)  # I2C object

    # Initialize LCD with default parameters (address 0x27, 2 rows, 16 columns, 5x8 font)
    lcd = LiquidCrystal_I2C(i2c)

    lcd.backlight(True)  # Backlight on
    lcd.clear_display()
    lcd.set_cursor(0, 0)
    lcd.print("Hello, World!")

    while True:
        for i in range(100):
            lcd.set_cursor(1, 0)
            lcd.print("       ")
            lcd.set_cursor(1, 0)
            lcd.print(i)
            utime.sleep_ms(500)


if __name__ == "__main__":
    main()
```

For more examples, see the [Examples](examples) directory.

## Simulation

The library supports simulation using the [WOKWI project](https://wokwi.com/projects/386814798911451137), enabling
hobbyist to test their code before deploying it to hardware.

## Class Methods

- `backlight(status: bool = False)`, `backlight(pin: int, status: bool = False)`: Control the backlight of the LCD.
- `clear_display()`: Clear the entire display.
- `return_home()`: Set the cursor to the home position.
- `display_on()`, `display_off()`: Turn on or off the display.
- `display_cursor()`, `display_no_cursor()`: Show or hide the cursor on the display.
- `cursor_blink()`, `cursor_no_blink()`: Enable or disable cursor blinking.
- `display_shift_left()`, `display_shift_right()`: Shift the entire display to the left or right.
- `cursor_shift_left()`, `cursor_shift_right()`: Shift the cursor position to the left or right.
- `set_cursor(row: int, col: int)`: Set the cursor to the specified row and column.
- `print(data: any)`: To print the given data on the LCD, `print(chr(custom_char))`: To print custom character on the
  LCD.
- `custom_character(ram_addr: int, bit_map: list | tuple)`: Define a custom character at the specified CGRAM address
  with the given bit map.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

இந்த LiquidCrystal மென்பொருள் நூலகத்திற்கான பங்களிப்புகள் மிகவும் ஊக்குவிக்கப்படுகின்றன! உங்களுக்கு ஏதேனும் சிக்கல்கள்
ஏற்பட்டாலோ அல்லது
மேம்பாடுகளுக்கான பரிந்துரைகள் இருந்தாலோ, தயவுசெய்து 'சிக்கல்' ஒன்றை உருவாக்கவும் அல்லது இழுக்கும் கோரிக்கையைச்
சமர்ப்பிக்கவும்.

## License

This project is licensed under the [MIT License](LICENSE).
