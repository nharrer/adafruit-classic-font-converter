import re

FONT_NAME_CLASSIC = 'Classic5x8CP437'
FONT_NAME_CLASSIC_EURO = 'Classic5x8CP437Euro'
OUTPATH = 'fonts'
CHAR_WIDTH = 5
CHAR_HEIGHT = 8

class Char:
    rows = None

    def __init__(self):
        self.rows = bytearray()

    # Read symbols from classic Adafruit bitmap, which has 5 bytes per glyph. The bytes are the columns 1..5.
    def from_classic(self, bytes):
        if len(bytes) != CHAR_WIDTH:
            raise Exception(f'Char needs to be {CHAR_WIDTH} bytes wide!')

        self.rows = bytearray()

        # Each byte is a column of the symbol. So we need to rotate the columns into rows.
        bitpos = 1
        for _ in range(CHAR_HEIGHT):
            b = 0
            for i in range(CHAR_WIDTH):
                b = b << 1
                if (bytes[i] & bitpos) != 0:
                    b = b | 1

            b = b << 1
            self.rows.extend(bytearray([b]))

            bitpos = bitpos << 1

        pass

    def from_bitmap(self, bitmap):
        self.rows = []
        l = None
        for bitmaprow in bitmap:
            if l is None:
                l = len(bitmaprow)
            elif l != len(bitmaprow):
                raise Exception('All rows of the bitmap must have the same length')
            b = 0
            for c in bitmaprow:
                value = 0
                if c == '#':
                    value = 1

                b = b << 1
                b = b | value
            self.rows.extend(bytearray([b]))

    def __repr__(self):
        return 'Char(' + ','.join('{:02x}'.format(x) for x in self.rows) + ')'

    def __str__(self):
        lines = []
        for b in self.rows:
            lines.append(f'{b:08b}'.replace('0', '.').replace('1', '#'))
        return '\n'.join(lines)

    def bytes_per_row(self):
        return (CHAR_WIDTH + 7) // 8

def read_font(filename):
    data = ''
    with open(filename) as f:
        for line in f:
            data = data + ' ' + line.strip()

    result = re.search(r'\{(.*?)\}', data)
    if result is None:
        raise Exception('Data block not found!')
    data = result.group(1)

    chars = []
    cnt = 0
    inbytes = bytearray()
    while True:
        result = re.search(r'0x(..)', data)
        if result is None:
            break
        data = data[result.end():]

        inbytes.extend(bytearray.fromhex(result.group(1)))
        cnt = cnt + 1
        if cnt == 5:
            char = Char()
            char.from_classic(inbytes)
            chars.append(char)
            inbytes = bytearray()
            cnt = 0

    return chars

def dumpbitmaps(chars, filename):
    with open(filename, 'w') as f:
        idx = 0
        for char in chars:
            f.write(f'Char {idx:03d}:\n')
            f.write(str(char))
            f.write('\n\n')
            idx = idx + 1

def write_headerfile(chars, fontname, path):
    filename = path + '/' + fontname + '.h'
    with open(filename, 'w') as f:
        f.write(f'const uint8_t {fontname}Bitmaps[] PROGMEM = {{\n')
        idx = 0
        for char in chars:
            f.write(f'    /* Char {idx:03d} (0x{idx:02x})    */\n')
            f.write('    /* | 8 4 2 1 8 4 2 1 |*/\n')
            for b in char.rows:
                bstr = f'{b:08b}'.replace('0', ' .').replace('1', ' #')
                f.write(f'    /* |{bstr} |*/ 0x{b:02x},\n')
            idx = idx + 1
        f.write('};\n\n')

        f.write(f'const GFXglyph {fontname}Glyphs[] PROGMEM = {{\n')
        f.write('    // Index, W, H, xAdv, dX, dY}\n')

        w = 8       # bitmap x-size
        h = 8       # bitmap y-size
        xadv = 6    #
        xoffs = -2
        yoffs = -8
        rownr = 0
        for char in chars:
            index = rownr * 8
            f.write(f'    {{  {index: 5d}, {w}, {h},    {xadv},  {xoffs}, {yoffs} }}, // {rownr:03d}\n')
            rownr = rownr + 1
        f.write('};\n\n')

        f.write(f'const GFXfont {fontname} PROGMEM = {{\n')
        f.write(f'    (uint8_t  *){fontname}Bitmaps,\n')
        f.write(f'    (GFXglyph *){fontname}Glyphs,\n')
        f.write(f'    0, 255, 8 // ASCII start, ASCII end, y-Advance\n')
        f.write('};\n\n')

# read in fonts
chars = read_font('glcdfont.c')

# just for debugging
dumpbitmaps(chars, 'bitmaps.txt')

# Write the header file for the classic font (1:1)
write_headerfile(chars, FONT_NAME_CLASSIC, OUTPATH)

# Write a modified version with a copyright sign (two characters wide at
# position 001 and 002) and a euro sign at position 128.
bitmap_euro = [
    ".....###",
    "....#...",
    "...#.###",
    "...#.#..",
    "...#.###",
    "....#...",
    ".....###",
    "........"
]
chars[1].from_bitmap(bitmap_euro)
bitmap_euro = [
    "........",
    "..#.....",
    "...#....",
    "...#....",
    "...#....",
    "..#.....",
    "........",
    "........"
]
chars[2].from_bitmap(bitmap_euro)
bitmap_euro = [
    "....##..",
    "...#..#.",
    "..###...",
    "...#....",
    "..###...",
    "...#..#.",
    "....##..",
    "........"
]
chars[128].from_bitmap(bitmap_euro)
write_headerfile(chars, FONT_NAME_CLASSIC_EURO, OUTPATH)

print(f'Done! Converted {len(chars)} Characters')
