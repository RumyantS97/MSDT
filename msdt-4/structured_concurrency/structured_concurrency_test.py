from asyncio import TaskGroup, timeout, sleep, gather
from image_processing import get_starting_image, get_gray_image, get_contrast_image, get_monochromatic_image, get_matrix_filter_image
from showing_image import display_image
from PIL import Image, ImageColor

async def get_image_list() -> [Image]:
    images = []
    starting_image = await get_starting_image()
    
    gray_image_task = get_gray_image(starting_image)
    contrast_image_task = get_contrast_image(gray_image_task)

    gray_image, contrast_image = await gray_image_task, await contrast_image_task

    monochromatic_image_task = get_monochromatic_image(gray_image, 0.12)
    smooth_image_task = get_matrix_filter_image(
        gray_image, 
        [
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ],
        0,
        1/16
    )
    relief_image_task = get_matrix_filter_image(
        gray_image, 
        [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, -1]
        ],
        0.5,
        1/2
    )
    res = await gather(
        monochromatic_image_task,
        smooth_image_task,
        relief_image_task
    )
    images.append([starting_image, gray_image, contrast_image, res])
    return images
