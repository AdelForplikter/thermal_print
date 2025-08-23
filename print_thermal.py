from escpos.printer import Win32Raw

# """ Receipt Printer T20III Definitions (EPSON T20III Receipt) """
# Epson = Win32Raw("EPSON TM-T20III Receipt")
Epson = Win32Raw("POSPrinter POS80")
# If you want to use Usb in windows, open computer management - Universial Serial 
# Bus Controllers. Find correct printer and right click properties. Then under 
# Hardware Ids you can find the idVendor and idProduct. They look like this: 
# USB\VID_1FC9&PID_2016&REV_0200
#
# idVendor = 0x1FC9
# idProduct = 0x2016
Epson.set(custom_size=True, align='left', width=1, height=1)

# The font from escpos is trash. Create full images instead. marta_klistre is an example


def print_40x30_sticker_to_thermal_printer(image_path):
    # marta_klistre is 320x264 pixels. In 203 DPI, this is 40x33 mm. There is some 
    # room between the stickers which are 40x30mm. Make the image to cover the blank 
    # space as well when creating images. 
    try:

        Epson._raw(b'\x1B\x40') # Initialize printer
        Epson.image(image_path, impl="bitImageRaster", center=True, high_density_horizontal=True, high_density_vertical=True)
        # Epson._raw(b'\x1D\x56\x00') # Cutting. Hard to implement
        print("success")

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")

print_40x30_sticker_to_thermal_printer("c:\\Users\\ano\\Downloads\\marta_klistre.png")
