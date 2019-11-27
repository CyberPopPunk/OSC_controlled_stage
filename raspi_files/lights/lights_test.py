import board
import neopixel

led_count = 24
gpio_pin = board.D18

led = neopixel.NeoPixel(gpio_pin, led_count,auto_write=False, pixel_order=ORDER)

#set order of LEDs on each pixel (set to RGB if broken)
ORDER = neopixel.RGB

