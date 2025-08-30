from p01_print_thermal import *;
from p02_image_generation import *;



# def thermal_print(printer, headline, text, inspect_image_only=False, width=320):
#     print(f"Printing to {printer}: {headline} - {text}")
# # thermal_print(printer="EPSON TM-T20III Receipt", headline="Klær",text="Sokker",inspect_image_only=True)

### Yellow Stcicker 40mm x 30mm
# print_sticker_to_thermal_printer(
#     printer=2, 
#     cut=True,
#     image_path=create_image(height=287, 
#                             width=320,
#                             marginleft=30,
#                             margintop=0, 
#                             headline="Mette Marit",
#                             text="Det var en gang en prinsesse\npå Quart. Hennes far, Sven O \nvar ikke konge."))
print_sticker_to_thermal_printer(
    printer=2, 
    cut=True,
    image_path=create_image(height=287, 
                            width=320,
                            marginleft=0,
                            margintop=0, 
                            headline="ZX-S4 Boost\nDC-DC Converter",
                            text="Input: 2V-24V, Output: 3V-30V\nMax 15A in, 4A out\nR22=5.6kohm for LiPo\nR22=12500/(U-0.75V)"))

                            # headline="DC-DC Converter\nXL6019 Step-up",
                            # text="Input: 3V-35V, Output: 5V-40V \n Does not step down"
