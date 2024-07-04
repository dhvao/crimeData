from PIL import Image, ImageFile
import os

def load_images(image_paths):
    """
    Loads images from given paths and ensures they are in RGBA format to handle transparency.
    """
    images = []
    for image_path in image_paths:
        if image_path.lower().endswith(".png"):
            try:
                img = Image.open(image_path).convert("RGBA")
                images.append(img)
            except FileNotFoundError:
                print(f"Error: File not found - {image_path}")
            except IOError:
                print(f"Error: Could not open - {image_path}")
        else:
            print(f"Skipping non-PNG file: {image_path}")
    return images

def combine_images(images, output_path, max_images_per_row=4):
    """
    Combines images into one large image based on the specified row limits.
    """
    if not images:
        print("No images to combine.")
        return

    total_rows = (len(images) + max_images_per_row - 1) // max_images_per_row
    row_heights = [max(img.height for img in images[row * max_images_per_row:(row + 1) * max_images_per_row])
                   if images[row * max_images_per_row:(row + 1) * max_images_per_row] else 0
                   for row in range(total_rows)]
    max_width = sum(img.width for img in images[:max_images_per_row])

    total_height = sum(row_heights)
    combined_image = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))

    x_offset, y_offset = 0, 0
    for i, img in enumerate(images):
        combined_image.paste(img, (x_offset, y_offset))
        x_offset += img.width
        if (i + 1) % max_images_per_row == 0:
            x_offset = 0
            y_offset += row_heights[i // max_images_per_row]

    try:
        combined_image.save(output_path, "PNG")
        print(f"Combined image saved to: {output_path}")
    except IOError as e:
        print(f"Error saving the combined image: {e}")

def combine_pngs_from_folder(folder_path, output_filename="combined_images.png", max_images_per_row=4):
    """
    Combines all PNG images from a folder into a single image.
    """
    image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.png')]
    images = load_images(image_paths)
    combine_images(images, os.path.join(folder_path, output_filename), max_images_per_row)

# Example usage
folder_path = "/path/to/images"
output_filename = "combined_images.png"
combine_pngs_from_folder(folder_path, output_filename, max_images_per_row=4)
