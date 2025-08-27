from p01_print_thermal import *;
from p02_image_generation import *;



def thermal_print(printer, headline, text, inspect_image_only=False, width=320):
    print(f"Printing to {printer}: {headline} - {text}")


thermal_print(printer="EPSON TM-T20III Receipt", headline="Klær",text="Sokker",inspect_image_only=True)