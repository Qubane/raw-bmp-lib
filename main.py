from random import random


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

    # pixel data
    for y in range(height):
        for x in range(width):
            red = (image[y][x] >> 16) & 255
            green = (image[y][x] >> 8) & 255
            blue = image[y][x] & 255

            data += bytearray([blue, green, red] + padding)

    return data


def main():
    image = [[0 for _ in range(128)] for _ in range(128)]

    for y in range(128):
        for x in range(128):
            image[y][x] = int(x / 128 * 255) * 65536 + int(y / 128 * 255)

    with open("test.bmp", "wb") as file:
        file.write(make_bitmap(image, 24))


if __name__ == '__main__':
    main()
