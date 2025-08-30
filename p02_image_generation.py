from datetime import datetime
from tkinter import font
from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile

def create_image(width=320, height=240, headline="", text="Normal Text", cut=False, headlinesize=32, textsize=22, marginleft=10, margintop=5):
    # Default size: 203dpi -> 40mm x 30mm = 320 x 240
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
        bbox = draw.textbbox((marginleft, margintop), headline, font=font_headline)
        bbox2 = draw.textbbox((marginleft, margintop + headlinesize), text, font=font_text)
        print(f'bbox (left,top,right,bottom): {bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, Total (width,height): {bbox[2] - bbox[0]},{bbox[3] - bbox[1]}')
        print('----')
        print(f'bbox2 (left,top,right,bottom): {bbox2[0]}, {bbox2[1]}, {bbox2[2]}, {bbox2[3]}, Total (width,height): {bbox2[2] - bbox2[0]},{bbox2[3] - bbox2[1]}')
        # ---

        if headline:
            draw.text((marginleft, margintop), headline, font=font_headline, fill=text_color)
        if text:
            draw.text((marginleft, margintop + bbox[3] - bbox[1] + 10), text, font=font_text, fill=text_color)

        # Draw emojis
        # draw.text((marginleft, ((bbox[3] - bbox[1]) + (bbox2[3] - bbox2[1]) + margintop + 20 )), "🧯🧯🧯", font=font_emoji, fill=text_color)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file.name, "PNG")
        temp_file.close()

        print(f"Task card image created: {temp_file.name}")
        return temp_file.name
    except Exception as e:
        print(f"Error creating image: {e}")
        return None

