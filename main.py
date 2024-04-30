from enum import Enum


class BitDepth(Enum):
    bpp1 = 1    # monochrome
    bpp4 = 4    # 16 color palette
    bpp8 = 8    # 256 color palette
    bpp16 = 16  # rgb565 (5 red | 6 green | 5 blue)
    bpp24 = 24  # rgb888 (8 red | 8 green | 8 blue)
    bpp32 = 32  # rgba (8 red | 8 green | 8 blue | 8 alpha)

    # aliases
    monochrome = 1
    pal4 = 4
    pal8 = 8
    rgb565 = 16
    rgb = 24
    rgb888 = 24
    rgba = 32


class Color:
    """
    Color class. Holds RGBA values as floats.
    """

    def __init__(self, r: float = 0, g: float = 0, b: float = 0, a: float = 0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @property
    def rgb565(self):
        return (int(self.r * 31) << 11) + (int(self.g * 63) << 5) + int(self.b * 31)

    @property
    def rgb888(self):
        return (int(self.r * 255) << 16) + (int(self.g * 255) << 8) + int(self.b * 255)


def make_bitmap(image: list[list[int]], bpp: BitDepth, palette: list[Color] | None = None) -> bytes:
    """
    Returns a bitmap image bytes
    """

    # make file data array
    data = bytearray()

    # image width and height
    width = len(image[0])
    height = len(image)

    # filesize
    filesize = int(width * height * bpp.value / 8)

    # file header
    data += b'BM'  # Signature
    data += filesize.to_bytes(4, 'little')  # FileSize
    data += (0).to_bytes(4)  # reserved
    data += (54).to_bytes(4, 'little')  # DataOffset

    # info header
    data += (40).to_bytes(4, 'little')  # size
    data += width.to_bytes(4, 'little')  # width
    data += height.to_bytes(4, 'little')  # height
    data += (1).to_bytes(2, 'little')  # planes
    data += bpp.value.to_bytes(2, 'little')  # Bits Per Pixel
    data += (0).to_bytes(4)  # Compression
    data += (0).to_bytes(4)  # ImageSize
    data += (0).to_bytes(4)  # XpixelsPerM
    data += (0).to_bytes(4)  # YpixelsPerM
    data += (0).to_bytes(4)  # Colors Used
    data += (0).to_bytes(4)  # Important Colors

    # padding amount
    padding = int((4 - ((width * bpp.value / 8) % 4)) % 4)
    padding = bytearray([0 for _ in range(padding)])

    # if the palette is used
    if bpp.value <= 8 and palette is not None and len(palette) == (2 ** bpp.value):
        # append the palette
        for color in palette:
            data += color.rgb888.to_bytes(4, 'little')

    # when no palette
    elif bpp.value > 8:
        pass

    # if there is some kind of error when decoding the palette
    else:
        raise Exception("Incorrect palette")



    return bytes(1)


def main():
    width = 128
    height = 128

    image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            image[y][x] = x

    with open("test.bmp", "wb") as file:
        bitmap = make_bitmap(
            image,
            BitDepth.monochrome,
            [
                Color(0, 0, 0),
                Color(1, 1, 1)
            ]
        )
        file.write(bitmap)


if __name__ == '__main__':
    main()
