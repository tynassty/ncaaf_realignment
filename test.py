import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


if __name__ == "__main__":
    old_image = Image.open("images/hrrrdrrr.jpg")
    width, height = old_image.size
    distorted_image = old_image.resize((width, height//2))
    new_image = Image.new("RGB", (width, height*2))
    new_image.paste(old_image, (0, 0))
    new_image.paste(distorted_image, (0, height))
    new_image.paste(distorted_image, (0, int(height*1.5)))
    new_image.show()

