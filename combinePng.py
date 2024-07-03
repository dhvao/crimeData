from PIL import Image, ImageFile
import os

def combine_pngs(image_paths, output_path, max_images_per_row=4):
    """
    Combines multiple PNG images into a single PNG image with a specified layout.

    Args:
        image_paths (list): A list of paths to the PNG images to be combined.
        output_path (str): The path to save the combined image.
        max_images_per_row (int, optional): The maximum number of images to place in each row. Defaults to 4.
    """

    # Check if any PNG files were provided
    if not image_paths:
        print("Error: No PNG image paths provided.")
        return

    images = []
    total_width = 0
    total_height = 0

    # Load and optionally resize images (consider adjusting maximum size for better quality)
    for image_path in image_paths:
        try:
            # Check if the file is a PNG file
            if image_path.lower().endswith(".png"):
                img = Image.open(image_path).convert("RGBA")  # Handle transparent backgrounds
                # img.thumbnail((256, 256), Image.ANTIALIAS)  # Optional: Resize each image to a maximum size
                images.append(img)
                total_height = max(total_height, img.height)
            else:
                print(f"Skipping non-PNG file: {image_path}")
        except FileNotFoundError:
            print(f"Error: File not found: {image_path}")

    # Calculate total rows based on total images and max per row
    total_images = len(images)
    total_rows = (total_images + max_images_per_row - 1) // max_images_per_row

    # Calculate total width and height for the combined image
    row_heights = [max(img.height for img in images[i * max_images_per_row:(i + 1) * max_images_per_row]) for i in range(total_rows)]
    total_width = sum(img.width for img in images[:max_images_per_row])
    total_height = sum(row_heights)

    # Create the combined image based on total size
    combined_img = Image.new("RGBA", (total_width, total_height), color=(255, 255, 255, 0))

    x_offset = 0
    y_offset = 0

    # Place images in the combined image
    for i, img in enumerate(images):
        combined_img.paste(img, (x_offset, y_offset))
        x_offset += img.width
        if (i + 1) % max_images_per_row == 0:
            x_offset = 0
            y_offset += row_heights[i // max_images_per_row]

    # Save the combined image
    try:
        combined_img.save(output_path, "PNG")
        print(f"Combined image saved to: {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def combine_pngs_from_folder(folder_path, output_filename="combined_images.png", max_images_per_row=4):
    """
    Combines all PNG images from a folder into a single PNG image with a specified layout.

    Args:
        folder_path (str): The path to the folder containing the PNG images.
        output_filename (str, optional): The filename for the combined image. Defaults to "combined_images.png".
        max_images_per_row (int, optional): The maximum number of images to place in each row. Defaults to 4.
    """

    # Get all PNG image paths in the folder
    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)
                   if filename.lower().endswith(".png")]

    # Combine the images with the folder path and output filename
    combine_pngs(image_paths, os.path.join(folder_path, output_filename), max_images_per_row)

# Example usage (replace with your folder path and desired output filename)
folder_path = "/Users/dhvao/Desktop/Dissertation/pie_charts"
output_filename = "combined_images.png"
combine_pngs_from_folder(folder_path, output_filename, max_images_per_row=4)
