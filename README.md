# RFID Scanner

This Python script uses the Adafruit PN532 library to read RFID tags and perform actions based on the tag read. It also includes audio and visual feedback using pygame and NeoPixel LEDs.

## Dependencies

- Python 3
- Adafruit PN532 library
- pygame
- NeoPixel

## Features

- Reads RFID tags using the PN532 RFID/NFC reader.
- Plays a sound when a tag is read.
- Displays a swirling light effect on a strip of NeoPixel LEDs when a tag is read.
- Changes the color of the LEDs based on whether the tag read matches a predefined valid tag.

## Usage

1. Install the required dependencies.
2. Set the `VALID_UID` variable in the script to the UID of the tag you want to consider as valid.
3. Run the script: `python scanner.py`

## Functions

- `initialize_audio()`: Initializes the pygame mixer for audio playback.
- `play_sound()`: Plays a sound file.
- `swirl_effect(pixels, cycles)`: Creates a swirling light effect on the NeoPixel strip.
- `brightness_transition(pixels, target_brightness, duration)`: Gradually changes the brightness of the NeoPixel strip over a specified duration.
- `turn_off_pixels(pixels)`: Turns off all the pixels on the NeoPixel strip.
- `pulsing_blue_thread(pixels)`: Creates a pulsing blue light effect on the NeoPixel strip in a separate thread.
- `read_rfid()`: Initializes the PN532 reader, reads RFID tags, and performs actions based on the tag read.

## Note

This script is intended for use with a specific hardware setup. Ensure your hardware matches the requirements of the script before running.
