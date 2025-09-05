import threading
from flask import Flask, render_template, request
# from escpos.printer import Win32Raw
from escpos.printer import Usb
import base64
import io
from PIL import Image, ImageDraw, ImageFont
import tempfile

def create_image(width=320, height=240, headline="", text="Normal Text", cut=False, headlinesize=32, textsize=22, marginleft=10, margintop=5):
    try:
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font_headline_path = "./static/fonts/arialbd.ttf"
        font_text_path = "./static/fonts/arial.ttf"
        font_emoji_path = "./static/fonts/seguiemj.ttf"

        font_headline_size = headlinesize # Default = 32
        font_text_size = textsize # Default = 22
        font_headline = ImageFont.truetype(font_headline_path, font_headline_size)
        font_text = ImageFont.truetype(font_text_path, font_text_size)
        font_emoji = ImageFont.truetype(font_emoji_path, font_headline_size)
        
        text_color = (0,0,0) # Black

        bbox = draw.textbbox((marginleft, margintop), headline, font=font_headline)
        bbox2 = draw.textbbox((marginleft, margintop + headlinesize), text, font=font_text)
        if headline:
            draw.text((marginleft, margintop), headline, font=font_headline, fill=text_color)
        if text:
            draw.text((marginleft, margintop + bbox[3] - bbox[1] + 10), text, font=font_text, fill=text_color)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file.name, "PNG")
        temp_file.close()
        with open(temp_file.name, "rb") as f:
            img_byte_arr = io.BytesIO(f.read())
        encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        print(f"Task card image created: {temp_file.name}")
        return temp_file.name, encoded_image
    except Exception as e:
        print(f"Error creating image: {e}")
        return None


def print_sticker_to_thermal_printer(printer=1, image_path=None, cut=False):
    if not image_path:
        print("No image path provided.")
        pass

    try:
        if printer == 1:
            # Epson = Win32Raw("POSPrinter POS80")
            Epson = Usb(idVendor=0x1FC9, idProduct=0x2016)  
        elif printer == 2:
            # Epson = Win32Raw("EPSON TM-T20III Receipt")
            Epson = Usb(idVendor=0x04b8, idProduct=0x0E28)

        Epson._raw(b'\x1B\x40') # Initialize printer
        Epson.set(custom_size=True, align='left', width=1, height=1)
        Epson.image(image_path, impl="bitImageRaster", high_density_horizontal=True, high_density_vertical=True)
        if cut:
            Epson._raw(b'\x1D\x56\x00') # Cutting. Hard to implement a precise cut
        Epson.close()
        print("success")
        pass

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")
        pass


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('escpos_printing.html')

@app.route('/submit', methods=['POST'])
def submit():
    width = request.form.get('width', 320, type=int)
    height = request.form.get('height', 240, type=int)
    headline = request.form.get('headline', '')
    text = request.form.get('text', 'Normal Text')
    cut = request.form.get('cut') == 'True'
    headlinesize = request.form.get('headlinesize', 32, type=int)
    textsize = request.form.get('textsize', 22, type=int)
    marginleft = request.form.get('marginleft', 10, type=int)
    margintop = request.form.get('margintop', 5, type=int)
    printer = request.form.get('printer', 1, type=int)

    image_path, encoded_image = create_image(width, height, headline, text, cut, headlinesize, textsize, marginleft, margintop)

    # Print the sticker to a thermal printer
    # print_sticker_to_thermal_printer(printer, image_path, cut)
    threading.Thread(target=print_sticker_to_thermal_printer, args=(printer, image_path, cut)).start()
    return render_template('results.html', encoded_image=encoded_image)

if __name__ == '__main__':
    app.run(debug=True)
