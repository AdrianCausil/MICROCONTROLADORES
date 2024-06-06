import sys
import time
import digitalio
import busio
import board
from adafruit_st7735r import ST7735R
import displayio
import terminalio
from adafruit_display_text import label
from collections import deque
from adafruit_ov7670 import (
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
)
uart = busio.UART(board.GP16, board.GP17,baudrate=115200,bits=8,parity=None,stop=2)
bufw= bytearray(10)
# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus
s=0
mosi_pin = board.GP19
clk_pin = board.GP18
reset_pin = board.GP22
cs_pin = board.GP26
dc_pin = board.GP28
displayio.release_displays()

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = ST7735R(display_bus, width=128, height=160, bgr=True)

splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 160, 1)

color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(125, 155, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)

cam_bus = busio.I2C(board.GP21, board.GP20)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True

buf = bytearray(2 * cam.width * cam.height)

chars = b" NNN||||||"

width = cam.width
row = bytearray(2 * width)

# Lista predefinida para la evaluación de desviación
predefined_list =bytearray(b'||||||||||NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN||||||||||')

# Variables para almacenar los últimos tres conjuntos de bytes
last_rows = [None, None, None]

# Crear la etiqueta de texto fuera del bucle
text_group = displayio.Group(scale=1, x=11, y=24)
text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF)
text_group.append(text_area)
splash.append(text_group)  # Agregar la etiqueta al grupo principal
def calcular_desviacion(bytearray_1, bytearray_2, bytearray_3, predefined_list):
    # Contar la cantidad de diferencias entre los bytearrays dados y el bytearray predefinido
    diferencias = sum(1 for i in range(len(predefined_list)) if bytearray_1[i] != predefined_list[i] or bytearray_2[i] != predefined_list[i] or bytearray_3[i] != predefined_list[i])
    # Calcular la desviación en porcentaje
    desviacion_porcentaje = (diferencias / len(predefined_list)) * 100
    
    # Determinar si la desviación es negativa o positiva
    if bytearray_1 < predefined_list:
        desviacion_porcentaje *= -1
    elif bytearray_1 > predefined_list:
        desviacion_porcentaje *= 1
    
    return desviacion_porcentaje
while True:
    desv=100
    cam.capture(buf)
    pant_row = []
    # Actualizar los últimos tres conjuntos de bytes
    last_rows[2] = last_rows[1]
    last_rows[1] = last_rows[0]
    last_rows[0] = bytearray(row)
    if last_rows[0] is not None and last_rows[1] is not None and last_rows[2] is not None:
        desv=calcular_desviacion(last_rows[2],last_rows[1],last_rows[0],predefined_list)

        

        #print("Cantidad de caracteres diferentes entre las últimas tres listas y la lista predefinida:", differences_1, ",", differences_2, ",", differences_3)

    # Actualizar el texto de la etiqueta con el contenido de row
    text = ""
    for j in range(cam.height-3,cam.height):
        for i in range(cam.width):
            row[i * 2] = row[i * 2 + 1] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]
    msg= str(int(desv))
    if msg != None:
        data=msg.encode(5)
        uart.write(data)
    
    text += row.decode() + "\n"
    text_area.text = text  # Actualizar el texto de la etiqueta

 