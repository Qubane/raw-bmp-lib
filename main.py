from enum import Enum


class BitDepth(Enum):
    bpp1 = 1    # monochrome
    bpp4 = 4    # 16 color palette
    bpp8 = 8    # 256 color palette
    bpp16 = 16  # rgb565 (5 red | 6 green | 5 blue)
    bpp24 = 24  # rgb888 (8 red | 8 green | 8 blue)
    bpp32 = 32  # rgba (8 red | 8 green | 8 blue | 8 alpha)


def rbg888_to_rgb565(r: int, g: int, b: int) -> tuple[int, int, int]:
    """
    Converts rgb888 to rgb565
    """

    red = int(r / 255 * 31)
    green = int(g / 255 * 63)
    blue = int(b / 255 * 31)

    return red, green, blue


def float_rgb_to_rgb888(r: float, g: float, b: float) -> tuple[int, int, int]:
    """
    Converts float rgb values to rgb888. Each component is in range 0 - 1
    """

    return int(r * 255), int(g * 255), int(b * 255)


def float_rgb_to_rgb565(r: float, g: float, b: float) -> tuple[int, int, int]:
    """
    Converts float rgb values to rgb888. Each component is in range 0 - 1
    """

    return int(r * 31), int(g * 63), int(b * 31)


def combine_rgb888(r: int, g: int, b: int) -> int:
    """
    Combines rgb888 into 1 value
    """

    return (r << 16) + (g << 8) + b


def combine_rgb565(r: int, g: int, b: int) -> int:
    """
    Combines rgb565 into 1 value
    """

    return (r << 11) + (g << 5) + b


def make_bitmap(image: list[list[int]], bpp: BitDepth) -> bytes:
    """
    Returns a bitmap image bytes
    """

    data = bytearray()

    # image width and height
    width = len(image[0])
    height = len(image)

    # filesize
    filesize = width * height * bpp // 8

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
    data += bpp.to_bytes(2, 'little')  # Bits Per Pixel
    data += (0).to_bytes(4)  # Compression
    data += (0).to_bytes(4)  # ImageSize
    data += (0).to_bytes(4)  # XpixelsPerM
    data += (0).to_bytes(4)  # YpixelsPerM
    data += (0).to_bytes(4)  # Colors Used
    data += (0).to_bytes(4)  # Important Colors

    # padding amount
    padding = int((4 - ((width * bpp / 8) % 4)) % 4)
    padding = bytearray([0 for _ in range(padding)])

    print(padding)

    return bytes(1)


def main():
    width = 3
    height = 128

    image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            color = float_rgb_to_rgb565(x / width, y / height, 0)
            image[y][x] = combine_rgb565(*color)

    with open("test.bmp", "wb") as file:
        file.write(make_bitmap(image, 8))


if __name__ == '__main__':
    main()
