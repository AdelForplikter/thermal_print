from datetime import datetime
from tkinter import font
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

# width 40mm = 320
# height 30mm = 240

# 203dpi -> 40mm x 30mm = 320 x 240
def create_image(width=320, height=240, headline="", text="Normal Text", cut=False, headlinesize=32, textsize=22, marginleft=10, margintop=5):
    try:
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font_headline_path = "C:/Windows/Fonts/arialbd.ttf"
        font_text_path = "C:/Windows/Fonts/arial.ttf"
        font_emoji_path = "C:/Windows/Fonts/seguiemj.ttf"

        font_headline_size = headlinesize # Default = 32
        font_text_size = textsize # Default = 22
        font_headline = ImageFont.truetype(font_headline_path, font_headline_size)
        font_text = ImageFont.truetype(font_text_path, font_text_size)
        font_emoji = ImageFont.truetype(font_emoji_path, font_headline_size)
        
        text_color = (0,0,0) # Black

        # --- Check how big the text is in the image. Consider implementing a warning if it's too big
        # bbox = draw.textbbox((marginleft, margintop), headline, font=font_headline)
        # bbox2 = draw.textbbox((marginleft, margintop + headlinesize), text, font=font_text)
        # print(f'bbox (left,top,right,bottom): {bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, Total (width,height): {bbox[2] - bbox[0]},{bbox[3] - bbox[1]}')
        # print('----')
        # print(f'bbox2 (left,top,right,bottom): {bbox2[0]}, {bbox2[1]}, {bbox2[2]}, {bbox2[3]}, Total (width,height): {bbox2[2] - bbox2[0]},{bbox2[3] - bbox2[1]}')
        # ---

        if headline:
            draw.text((marginleft, margintop), headline, font=font_headline, fill=text_color)
        if text:
            draw.text((marginleft, margintop + font_headline_size), text, font=font_text, fill=text_color)
        draw.text((marginleft, ((bbox[3] - bbox[1]) + (bbox2[3] - bbox2[1]) + margintop + 20 )), "🧯🧯🧯", font=font_emoji, fill=text_color)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file.name, "PNG")
        temp_file.close()

        print(f"Task card image created: {temp_file.name}")
        return temp_file.name
    except Exception as e:
        print(f"Error creating image: {e}")
        return None


def create_task_image(task_data): # From CodingwithLewis image_generator.py

    try:
        width = 576  # 72mm thermal printer width
        # Load fonts first to calculate sizes
        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            date_font = ImageFont.truetype("arial.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            date_font = ImageFont.load_default()

        # Calculate content height
        title_lines = textwrap.wrap(task_data["title"], width=15)
        title_height = len(title_lines) * 95 + 10
        emoji_height = 150
        date_height = 40
        total_padding = 30
        
        height = title_height + emoji_height + date_height + total_padding

        # Create image with white background
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)

        # Draw title at the top
        title_y = 10
        
        for i, line in enumerate(title_lines):
            line_bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            draw.text((line_x, title_y + i * 95), line, fill="black", font=title_font)

        # Draw lightning bolt emoji after title
        emoji_y = title_y + len(title_lines) * 95 + 20
        
        # Try to use a font that supports emojis
        emoji_font = None
        font_paths = [
            "C:/Windows/Fonts/seguiemj.ttf",  # Segoe UI Emoji
            "C:/Windows/Fonts/segoeuiemoji.ttf",  # Alternative name
            "C:/Windows/Fonts/seguisym.ttf",  # Segoe UI Symbol
            "C:/Windows/Fonts/arial.ttf",  # Arial fallback
        ]
        
        for font_path in font_paths:
            try:
                emoji_font = ImageFont.truetype(font_path, 150)
                break
            except:
                continue
        
        # If no font found, use default
        if emoji_font is None:
            emoji_font = ImageFont.load_default()
        
        use_fallback = False
        
        if task_data["priority"].upper() == "HIGH":
            # Three lightning bolt emojis
            emoji_text = "🧯🎥📹"
        else:
            # Single lightning bolt emoji
            emoji_text = "⏳"
        
        # Calculate position to center the emoji
        emoji_bbox = draw.textbbox((0, 0), emoji_text, font=emoji_font)
        emoji_width = emoji_bbox[2] - emoji_bbox[0]
        emoji_x = (width - emoji_width) // 2
        draw.text((emoji_x, emoji_y), emoji_text, fill="black", font=emoji_font)

        # Draw due date below emoji
        date_y = emoji_y + 150
        due_date = datetime.now().strftime("%B %d")
        # Add ordinal suffix
        day = int(datetime.now().strftime("%d"))
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        due_date_text = f"{datetime.now().strftime('%B %d')}{suffix}"
        date_bbox = draw.textbbox((0, 0), due_date_text, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = (width - date_width) // 2
        draw.text((date_x, date_y), due_date_text, fill="black", font=date_font)

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_file.name, "PNG")
        temp_file.close()

        print(f"Task card image created: {temp_file.name}")
        return temp_file.name

    except Exception as e:
        print(f"error")
        return None

# create_task_image(task_data={"title": "Sample Task", "priority": "HIGH"})