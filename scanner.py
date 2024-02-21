import time
import board
import busio
import os
from adafruit_pn532.i2c import PN532_I2C
import neopixel

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame._sdl2.audio as sdl2_audio


valid = "04558c92ec5b80"
audio = True

# Pre init helps to get rid of sound lag
#pygame.mixer.pre_init(44100, -16, 1, 512 )
try:
   pygame.mixer.pre_init(44100,-16,1,512)
   pygame.mixer.get_init()
   pygame.mixer.init()
   devices = tuple(sdl2_audio.get_audio_device_names(False))
   print(devices)
   device = devices[0]
   pygame.mixer.init(devicename=device)
except Exception as error:
   print("No Audio")
   print(error)
   audio = False

# play sound
def playSound():
   if audio:
      pygame.mixer.music.set_volume(0.25)
      pygame.mixer.music.load("magicband_fastpass.mp3")
      print(pygame.mixer.music.get_volume())
      pygame.mixer.music.play()

def swirl_effect(pixels, cycles=12):
    num_pixels = len(pixels)
    for _ in range(cycles):
        for i in range(num_pixels -1, -1, -1):
            pixels[i] = (255, 255, 255)  # Full brightness for the current pixel

            # Calculate the indices of the neighbors
            left_neighbor = (i - 1) % num_pixels
            right_neighbor = (i + 1) % num_pixels
            l2 = (i-2) % num_pixels
            r2 =  (i+2) % num_pixels

            # Set the brightness of the neighbors to 50%
            pixels[left_neighbor] = (127, 127, 127)
            pixels[right_neighbor] = (127, 127, 127)
            pixels[l2] = (127,127,127)
            pixels[r2] = (127,127,127)

            pixels.show()
            if _ < 3:
               time.sleep(0.03)
            else:
               time.sleep(0.03 * (1/(_-1)))

            # Reset the pixels to 0 brightness
            pixels[i] = (0, 0, 0)
            pixels[left_neighbor] = (0, 0, 0)
            pixels[right_neighbor] = (0, 0, 0)
            pixels[l2] = (0,0,0)
            pixels[r2] = (0,0,0)

def brightness_transition(pixels, target_brightness, duration):
    start_brightness = pixels.brightness

    steps = int(duration / 0.1)  # 0.1 seconds per step
    brightness_step = (target_brightness - start_brightness) / steps

    for _ in range(steps):
        start_brightness += brightness_step
        pixels.brightness = start_brightness
        pixels.show()
        time.sleep(0.1)

def turn_off_pixels(pixels):
    num_pixels = len(pixels)
    for i in range(num_pixels):
        pixels[num_pixels - i - 1] = (0, 0, 0)
        pixels.show()
        time.sleep(0.05)

def pulsing_blue_effect(pixels, pulses=2):
    for _ in range(pulses):
        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(0.5)  # Adjust the duration of each pulse as needed

        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)

def read_rfid():
    i2c = busio.I2C(board.SCL, board.SDA)
    pn532 = PN532_I2C(i2c, address=0x24)
    #pixels = neopixel.NeoPixel(board.D18, 10)  # Change D18 to the pin you're using

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
       board.D18, 22, brightness=1, auto_write=False, pixel_order=ORDER
    )

    ic, ver, rev, support = pn532.firmware_version
    print(f"Found PN532 with firmware version: {ver}.{rev}")

    pn532.SAM_configuration()

    print("Pulsing blue lights to indicate readiness...")
    pulsing_blue_effect(pixels)

    print("Waiting for an RFID card...")

    while True:
        uid = pn532.read_passive_target(timeout=0.5)

        if uid is not None:
            print("Card detected with UID:", [hex(i) for i in uid])
            print(uid)
            print(uid.hex())
             
            print("swirling lights")
            swirl_effect(pixels)
		
            # Turn all lights solid green
            print("lights green")
            pixels.brightness = 0.01
            if uid.hex() == valid:
               pixels.fill((0, 255, 0))
            else:
               pixels.fill((255,0,0))
            pixels.show()
            
           # Increase brightness to 50% over 2 seconds
            playSound()
            brightness_transition(pixels, 1, 1)
            # Wait for a moment
            #time.sleep(1)

            # Fade off effect
            print("fade out")
            #brightness_transition(pixels, 0, 1) 
            turn_off_pixels(pixels)

            # Turn off all lights
            print("turn off")
            pixels.fill((0, 0, 0))
            pixels.brightness = 1.0
            pixels.show()

if __name__ == "__main__":
    read_rfid()
