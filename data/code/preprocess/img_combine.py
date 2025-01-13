from PIL import Image, ImageDraw, ImageFont
import os

def combine_images_with_numbers(folder_path, output_path):
    # List all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    
    if not image_files:
        print("No images found in the folder.")
        return

    image_files = sorted(image_files)

    images = []
    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        images.append(Image.open(img_path))

    # Load a font or use a default PIL font
    font = ImageFont.load_default(size=100)

    # Calculate total width and max height
    total_width = 0
    max_height = 0
    numbered_images = []

    for idx, img in enumerate(images):
        text = f"({idx + 1})"

        # Get text size using textbbox
        temp_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
        draw = ImageDraw.Draw(temp_img)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        margin = 20

        # Create a new image with space for the text on the left
        labeled_image = Image.new("RGBA", (img.width + text_width + margin * 3, img.height + margin * 2), (255, 255, 255, 255))
        labeled_image.paste(img, (text_width + margin * 2, margin))

        # Draw the red box around the image
        draw = ImageDraw.Draw(labeled_image)
        box_coords = (text_width + margin * 2, margin, text_width + margin * 2 + img.width, margin + img.height)
        draw.rectangle(box_coords, outline="red", width=5)

        # Draw the number on the left of the image
        draw.text((margin, (labeled_image.height - text_height) // 2), text, fill="black", font=font)

        numbered_images.append(labeled_image)
        total_width += labeled_image.width
        max_height = max(max_height, labeled_image.height)

    # Create the final combined image
    combined_image = Image.new("RGBA", (total_width, max_height), (255, 255, 255, 255))

    # Paste all numbered images side by side
    x_offset = 0
    for img in numbered_images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    # Save the final image
    combined_image.save(output_path)

if __name__ == "__main__":
    # Example usage
    folder_path = "data/goodui/0"
    output_path = "data/goodui/0/concat.png"
    font_path = None
    combine_images_with_numbers(folder_path, output_path)