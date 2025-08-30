from escpos.printer import Win32Raw

def print_sticker_to_thermal_printer(printer=1, image_path=None, cut=False):
    if not image_path:
        print("No image path provided.")
        return

    try:
        # """ Receipt Printer T20III Definitions (EPSON T20III Receipt) """
        if printer == 1:
            Epson = Win32Raw("POSPrinter POS80")
        elif printer == 2:
            Epson = Win32Raw("EPSON TM-T20III Receipt")

        Epson._raw(b'\x1B\x40') # Initialize printer
        Epson.set(custom_size=True, align='left', width=1, height=1)
        Epson.image(image_path, impl="bitImageRaster", high_density_horizontal=True, high_density_vertical=True)
        if cut:
            Epson._raw(b'\x1D\x56\x00') # Cutting. Hard to implement a precise cut
        print("success")

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")


