import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import Pulseox_Serial


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                     width=135, height=240, x_offset=53, y_offset=40)

height = disp.width   # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new('RGB', (width, height))
rotation = 90

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
padding = -2
top = padding
bottom = height-padding
x = 0

font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
recording = False
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
pulse_ox = Pulseox_Serial.PusleOx()

while True:
    if not buttonA.value:
        backlight.value = not backlight.value
    if not buttonB.value:
        recording = not recording
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    reading = pulse_ox.get_reading()
    if recording:
        reading.save_reading()

    line1 = reading.status_out()
    line2 = reading.heart_rate_out()
    line3 = reading.oxygen_out()
    line4 = f'{(not recording)*"not"} recording'
    line5 = reading.now_out()

    y = top
    draw.text((x, y), line1, font=font, fill="#FFFFFF")
    y += font.getsize(line1)[1]
    draw.text((x, y), line2, font=font, fill="#FFFF00")
    y += font.getsize(line2)[1]
    draw.text((x, y), line3, font=font, fill="#00FF00")
    y += font.getsize(line3)[1]
    draw.text((x, y), line4, font=font, fill="#0000FF")
    y += font.getsize(line4)[1]
    draw.text((x, y), line5, font=font, fill="#FF00FF")

    disp.image(image, rotation)
    time.sleep(.1)
