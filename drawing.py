from PIL import Image


def group_images(images: list[Image.Image], row_count=2, crop_empty_row=False):
    image_count = len(images)
    column_count = -(image_count // -row_count)
    widths = [image.width for image in images]
    heights = [image.height for image in images]
    unit_size = max(max(widths), max(heights))
    width = column_count * unit_size
    height = row_count * unit_size
    to_return = Image.new("RGB", (width, height))
    distributed_images = distribute(images, row_count)
    # for i in range(len(distributed_images)):
    #     row = distributed_images[i]
    #     to_return.paste(group_row(row, unit_size, column_count), (0, i * unit_size))
    for i in range(row_count):
        images_to_group = images[:column_count]
        if len(images_to_group) > 0 or not crop_empty_row:
            grouped_row = group_row(images_to_group, unit_size, column_count)
            to_return.paste(grouped_row, (0, i * unit_size))
            images = images[column_count:]
        else:
            to_return = to_return.crop((0, 0, width, unit_size * (row_count - 1)))
    return to_return


def group_row(input_images, unit_size, column_count):
    to_return = Image.new("RGB", (unit_size * column_count, unit_size))
    images_missing = column_count - (len(input_images) % column_count)
    if images_missing == column_count:
        images_missing = 0
    x_offset = images_missing * 0.5 * unit_size
    for i in range(len(input_images)):
        to_return.paste(input_images[i], ((unit_size * i) + int(x_offset), 0))
    return to_return


def distribute(objects, k):
    groups = [[] for _ in range(k)]
    for i in range(len(objects)):
        groups[i % k].append(objects[i])
    return groups


if __name__ == "__main__":
    images_list = [Image.open("images/hrrrdrrr.jpg") for _ in range(13)]
    group_image = group_images(images_list, 2)
    group_image.show()
