Adafruit Classic Font Converter
===============================

This is a simple python script which converts the classic built-in font of the [Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) into a GFX Font. This is useful if you'd like to use the classic font, but want to change some symbols.

Usage
-----

The resulting gfx font header files are already included in this repository in the fonts directory. So you don't need to convert them yourselfs:

| File                              | Description |
|-----------------------------------|-------------|
| ```fonts/Classic5x8CP437.h```     | The classic font just as it is (but see [Notes](##Notes))       |
| ```fonts/Classic5x8CP437Euro.h``` | The same but characters #001 and #002 are replaced with a copyright sign (two characters wide) and character #128 is replaced with a euro sign |

However if you want to do it yourself or want to override some characters, simply run the script convert.py with python 3:

> python convert.py

It reads the font glyphs from ```glcdfont.c``` (which is part of the Aafruit-GFX-Library) and write the GFX fonts into folder ```fonts```.

Notes
-----

The Adafruit-GFX-Library classic font is based on code page 437, but it has the character #176 (*light shade block*) missing. That means that all characters after #176 are shifted down one position. The converter however moves the characters to the *right* position.

