Adafruit Classic Font Converter
===============================

This is a simple python script which converts the classic built-in font of the [Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) into a GFX font. This is useful if you'd like to use the classic font, but want to change some symbols.

Usage
-----

The resulting gfx font header files are already included in this repository in the `fonts` directory. So you don't need to convert them yourself:

| File                              | Description |
|-----------------------------------|-------------|
| [`fonts/Classic5x8CP437.h`](https://raw.githubusercontent.com/nharrer/adafruit-classic-font-converter/main/fonts/Classic5x8CP437.h)         | The classic font just as it is (but see [Notes](#notes)).                                                                                           |
| [`fonts/Classic5x8CP437Euro.h`](https://raw.githubusercontent.com/nharrer/adafruit-classic-font-converter/main/fonts/Classic5x8CP437Euro.h) | The same, but characters #001 and #002 are replaced with a copyright sign (two characters wide) and character #128 is replaced with a euro sign. |

If you want to convert it yourself or want to override some characters, simply run the script [`convert.py`](https://github.com/nharrer/adafruit-classic-font-converter/blob/main/convert.py) with python 3:

```
python convert.py
```

It reads the font glyphs from [`glcdfont.c`](https://github.com/nharrer/adafruit-classic-font-converter/blob/main/glcdfont.c) (which is part of the Aafruit-GFX-Library) and writes the GFX fonts into folder `fonts`.

Notes
-----

The Adafruit-GFX-Library classic font is based on code page 437. But in default mode, it has the character #176 (*light shade block*) missing. That means all characters from #176 upwards are shifted down one position (unless enabling `.cp437(true)` on the gfx library object). The converter creates the characters at the *right* cp437 position however.
