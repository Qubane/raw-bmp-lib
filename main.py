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


def make_bitmap(image: list[list[int]], bpp: int = 24) -> bytes:
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
    padding = ((4 - ((width * (bpp // 8)) % 4)) % 4)
    padding = [0 for _ in range(padding)]

    # data reading
    if bpp == 1:
        def get_bytes(x_, y_):
            return bytearray([image[y_][x_] > 0] + padding)
    elif bpp == 4:
        def get_bytes(x_, y_):
            return bytes(0)
    elif bpp == 8:
        def get_bytes(x_, y_):
            return bytes(0)
    elif bpp == 16:  # rgb565
        def get_bytes(x_, y_):
            return (image[y_][x_] & 65535).to_bytes(2, 'little')
    elif bpp == 24:  # rgb888
        def get_bytes(x_, y_):
            return (image[y_][x_] & 16777215).to_bytes(3, 'little')
    elif bpp == 32:  # rgba
        def get_bytes(x_, y_):
            return (image[y_][x_] & 4294967295).to_bytes(4, 'little')
    else:
        raise NotImplementedError()

    # pixel data
    for y in range(height):
        for x in range(width):
            data += get_bytes(x, y)

    return data


def main():
    width = 128
    height = 128

    image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            red = x / width * 31
            green = y / height * 63
            blue = 0

            image[y][x] = (int(red) << 11) + (int(green) << 5) + int(blue)

    with open("test.bmp", "wb") as file:
        file.write(make_bitmap(image, 16))


if __name__ == '__main__':
    main()
