import cmath
from PIL import Image, ImageColor

import numpy as np

async def get_starting_image() -> Image:
    return Image.open("E:/ferry.jpg")

async def get_gray_image(image: Image) -> Image:
    image_array = np.array(image)
    image_height, image_width, channels = image_array.shape  # Assuming RGB image


    for y in range(0, image_height):
        for x in range(0, image_width):
            r, g, b = image_array[y, x]
            lightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
            for c in range(channels):
                image_array[y, x, c] = lightness

    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    return Image.fromarray(image_array)

async def get_contrast_image(image: Image) -> Image:
    image_array = np.array(image)
    image_height, image_width, channels = image_array.shape  # Assuming RGB image


    for y in range(0, image_height):
        for x in range(0, image_width):
            for c in range(channels):
                new_value = image_array[y, x, c] * 2 - 128
                image_array[y, x, c] = new_value

    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    return Image.fromarray(image_array)

async def get_monochromatic_image(image: Image, treshold: float) -> Image:
    image_array = np.array(image)
    image_height, image_width, channels = image_array.shape  # Assuming RGB image


    for y in range(0, image_height):
        for x in range(0, image_width):
            r, g, b = image_array[y, x]
            lightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
            for c in range(channels):
                image_array[y, x, c] = 255 if lightness > 255 * treshold else 0

    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    return Image.fromarray(image_array)

async def get_matrix_filter_image(image: Image, matrix: [[]], a: float, b: float) -> Image:
    image_array = np.array(image)
    image_height, image_width, channels = image_array.shape  # Assuming RGB image


    for y in range(1, image_height - 1):
        for x in range(1, image_width - 1):
            for c in range(channels):
                summ = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        summ += image_array[y + i, x + j, c] * matrix[i + 1][j + 1]
                image_array[y, x, c] = a + summ / b

    image_array = np.clip(image_array, 0, 255).astype(np.uint8)

    return Image.fromarray(image_array)