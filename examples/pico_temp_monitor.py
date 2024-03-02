import utime
from machine import ADC, I2C, Pin

from LiquidCrystal import LiquidCrystal_I2C


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    lcd = LiquidCrystal_I2C(i2c)
    sensor_temp = ADC(4)

    conversion_factor: float = 3.3 / 65535

    lcd.backlight(True)
    lcd.set_cursor(0, 0)
    lcd.print("Temperature")

    while True:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        lcd.set_cursor(1, 0)
        lcd.print("       ")  # For avoid. clearing entire display.
        lcd.set_cursor(1, 0)
        lcd.print(f"temp: {temperature:.2f}°C")
        utime.sleep_ms(60)  # Update the new readings.


if __name__ == "__main__":
    main()
