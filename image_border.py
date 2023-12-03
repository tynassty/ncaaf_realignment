import math
import random
from PIL import Image, ImageDraw

WHITE = (255, 255, 255, 255)


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def stickerify(input_path, output_path, radius):
    # Open the image
    img = Image.open(input_path).convert("RGBA")

    # Create a copy of the original image
    result_img = img.copy()

    # Get the pixel data
    original_pixels = img.load()
    pixels = result_img.load()

    # Iterate through each pixel
    for x in range(result_img.width):
        for y in range(result_img.height):
            print(x, y)
            # Check if the pixel is transparent or white
            if pixels[x, y][3] <= 254:
                # Check nearby pixels within the circular radius
                for i in range(max(0, x - radius), min(result_img.width, x + radius + 1)):
                    for j in range(max(0, y - radius), min(result_img.height, y + radius + 1)):
                        # Check if the nearby pixel is non-transparent and within the circular radius
                        if original_pixels[i, j][3] == 255 and distance(x, y, i, j) <= radius:
                            # Turn the transparent/white pixel to white
                            pixels[x, y] = (255, 255, 255, 255)
                            # transparency = 255 - int((distance(x, y, i, j) / radius) * 255)
                            # pixels[x, y] = (255, 255, 255, max(transparency, pixels[x, y][3]))
                            break

    # Save the result
    result_img.save(output_path)


if __name__ == "__main__":
    input_image_path = "images/Air_Force.png"
    output_image_path = "images/aaaaaaoutput.png"
    radius = 20
    stickerify(input_image_path, output_image_path, radius)
