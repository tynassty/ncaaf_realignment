from PIL import Image


def group_images(images: list[Image.Image], column_count=7, group_spacing=0.0):
    image_count = len(images)
    row_count = -(image_count // -column_count)
    widths = [image.width for image in images]
    heights = [image.height for image in images]
    # unit_size = max(max(widths), max(heights))
    unit_width = max(widths)
    unit_height = max(heights)
    offset = int(group_spacing * unit_height)
    total_width = unit_width * column_count
    total_height = int((unit_height * row_count) + (group_spacing * unit_height * row_count))
    to_return = Image.new("RGBA", (total_width, total_height), color=(255, 255, 255))
    for i in range(row_count):
        images_to_group = images[:column_count]
        grouped_row = group_row(images_to_group, unit_width, column_count)
        to_return.paste(grouped_row, (0, (i * unit_height) + (offset * i) + offset), grouped_row)
        images = images[column_count:]
    return to_return


def group_images_from_paths(image_paths: list[str], column_count=7):
    images = [Image.open(image_path) for image_path in image_paths]
    widths = [image.width for image in images]
    heights = [image.height for image in images]
    unit_size = max(max(widths), max(heights))
    for i in range(len(images)):
        image = images[i]
        image_w = widths[i]
        image_h = heights[i]
        if image_w != unit_size or image_h != unit_size:
            background = Image.new("RGBA", (unit_size, unit_size), color=(255, 255, 255, 255))
            background_w, background_h = background.size
            offset = ((background_w - image_w) // 2, (background_h - image_h) // 2)
            background.paste(image, offset)
            images[i] = background

    return group_images(images, column_count)


def group_row(input_images, unit_width, column_count):
    to_return = Image.new("RGBA", (unit_width * column_count, unit_width), color=(255, 255, 255))
    images_missing = column_count - (len(input_images) % column_count)
    if images_missing == column_count:
        images_missing = 0
    x_offset = images_missing * 0.5 * unit_width
    for i in range(len(input_images)):
        to_return.paste(input_images[i], ((unit_width * i) + int(x_offset), 0), mask=input_images[i])
    return to_return


def distribute(objects, k):
    groups = [[] for _ in range(k)]
    for i in range(len(objects)):
        groups[i % k].append(objects[i])
    return groups


if __name__ == "__main__":
    # images_list = [Image.open("images/South_Carolina.png") for _ in range(13)]
    # group_image = group_images(images_list, 7)
    # group_image.show()

    image_path_list = ["images/South_Carolina.png" for _ in range(13)]
    group_image = group_images_from_paths(image_path_list, 7)
    group_image.show()
