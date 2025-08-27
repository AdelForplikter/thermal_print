from escpos.printer import Win32Raw

# """ Receipt Printer T20III Definitions (EPSON T20III Receipt) """
Epson = Win32Raw("EPSON TM-T20III Receipt")
# Epson = Win32Raw("POSPrinter POS80")


Epson.set(custom_size=True, align='left', width=1, height=1)



def print_sticker_to_thermal_printer(image_path):
    try:
        Epson._raw(b'\x1B\x40') # Initialize printer
        Epson.image(image_path, impl="bitImageRaster", center=True, high_density_horizontal=True, high_density_vertical=True)
        # Epson._raw(b'\x1D\x56\x00') # Cutting. Hard to implement
        print("success")

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")

# print_sticker_to_thermal_printer("c:\\Users\\ano\\Downloads\\marta_klistre.png")
print_sticker_to_thermal_printer("C:\\Users\\ano\\AppData\\Local\\Temp\\tmp9qf6f55w.png")
