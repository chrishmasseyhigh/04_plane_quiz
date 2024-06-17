from PIL import Image
import os


def resize_and_pad(image, target_width, target_height, background_color=("white")):
    img_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_width = target_width
        new_height = round(target_width / img_ratio)
    else:
        new_width = round(target_height * img_ratio)
        new_height = target_height

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    new_image = Image.new("RGB", (target_width, target_height), background_color)
    paste_position = ((target_width - new_width) // 2, (target_height - new_height) // 2)
    new_image.paste(resized_image, paste_position)

    return new_image


def process_images(input_folder, output_folder, target_width, target_height):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".webp"):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path).convert("RGB")
            new_img = resize_and_pad(img, target_width, target_height)
            new_img.save(os.path.join(output_folder, filename), format='jpeg')


input_folder = "Plane_Images"
output_folder = "Resized_Plane_Images"
target_width = 640
target_height = 360

process_images(input_folder, output_folder, target_width, target_height)
