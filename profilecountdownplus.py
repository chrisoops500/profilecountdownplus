from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

def add_days_to_image(year, image_path, position, color):
    try:
        # Calculate the number of days until New Year's Day of the specified year
        today = datetime.now()
        new_year = datetime(int(year), 1, 1)
        days_remaining = (new_year - today).days

        if days_remaining < 0:
            print("Error: The entered year has already passed. Please enter a future year.")
            return

        # Generate the text to display
        text = f"{days_remaining} days to {year}"

        # Load the image
        image = Image.open(image_path)

        # Ensure the image is in RGB mode
        if image.mode != "RGB":
            image = image.convert("RGB")

        draw = ImageDraw.Draw(image)

        # Choose the font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Chalkduster.ttf", 40)
        except IOError:
            print("Warning: Chalkduster.ttf not found. Using the default font instead.")
            font = ImageFont.load_default()

        # Compute text bounding box
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Calculate text position
        image_width, image_height = image.size
        x_position = (image_width - text_width) // 2

        if position == "top":
            y_position = max(10, (image_height - text_height) // 10)
        elif position == "middle":
            y_position = (image_height - text_height) // 2
        else:  # bottom
            y_position = image_height - text_height - 20

        # Define color choices
        color_map = {"black": "black", "white": "white", "red": "red"}
        text_color = color_map.get(color, "black")  # Default to black if invalid input

        # Draw the text on the image
        draw.text((x_position, y_position), text, font=font, fill=text_color)

        # Save the modified image in the same directory as the original
        image_dir, image_name = os.path.split(image_path)
        modified_image_path = os.path.join(image_dir, "profile_countdown_plus.jpg")
        image.save(modified_image_path)

        print(f"Image successfully saved to: {modified_image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Get user input
year = input("Enter the target countdown year (e.g., 2026): ")
image_path = input("Enter the path of the image to process: ")

# Ensure the entered image path exists
if not os.path.exists(image_path):
    print("Error: The specified image file does not exist. Please check the path.")
else:
    position = input("Where do you want the text? (top/middle/bottom): ").strip().lower()
    if position not in ["top", "middle", "bottom"]:
        print("Invalid position. Defaulting to middle.")
        position = "middle"

    color = input("Choose text color (black/white/red): ").strip().lower()
    if color not in ["black", "white", "red"]:
        print("Invalid color. Defaulting to black.")
        color = "black"

    add_days_to_image(year, image_path, position, color)
