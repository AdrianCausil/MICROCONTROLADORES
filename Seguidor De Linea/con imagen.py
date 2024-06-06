import sys
import time
import digitalio
import busio
import board
from adafruit_st7735r import ST7735R
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_ov7670 import (
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
)

uart = busio.UART(board.GP16, board.GP17, baudrate=115200, bits=8, parity=None, stop=2)
bufw = bytearray(10)

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
predefined_list = bytearray(b'||||||||||NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN||||||||||')

# Variables para almacenar los últimos tres conjuntos de bytes
last_rows = [None, None, None]

# Crear un bitmap para mostrar las filas combinadas
combined_bitmap = displayio.Bitmap(128, 24, 3)
combined_palette = displayio.Palette(3)
combined_palette[0] = 0x000000  # Black
combined_palette[1] = 0x0000FF  # Blue for "|"
combined_palette[2] = 0xFF0000  # Red for "N"
combined_sprite = displayio.TileGrid(combined_bitmap, pixel_shader=combined_palette, x=0, y=68)  # Ajustar la posición según sea necesario
splash.append(combined_sprite)

# Crear la etiqueta de texto fuera del bucle
text_group = displayio.Group(scale=2, x=11, y=25)
text_area = label.Label(terminalio.FONT, text="", color=0xFFFFFF)
text_group.append(text_area)
splash.append(text_group)  # Agregar la etiqueta al grupo principal

def calcular_desviacion(bytearray_1, bytearray_2, bytearray_3, predefined_list):
    diferencias = sum(1 for i in range(len(predefined_list)) if bytearray_1[i] != predefined_list[i] or bytearray_2[i] != predefined_list[i] or bytearray_3[i] != predefined_list[i])
    desviacion_porcentaje = (diferencias / len(predefined_list)) * 100
    
    if bytearray_1 < predefined_list:
        desviacion_porcentaje *= -1
    elif bytearray_1 > predefined_list:
        desviacion_porcentaje *= 1
    
    return desviacion_porcentaje

def update_display(text):
    text_area.text = text
    display.refresh()

def transmit_uart(data):
    uart.write(data)

while True:
    cam.capture(buf)
    pant_row = []
    
    last_rows[2] = last_rows[1]
    last_rows[1] = last_rows[0]
    last_rows[0] = bytearray(row)
    
    if last_rows[0] is not None and last_rows[1] is not None and last_rows[2] is not None:
        desv = calcular_desviacion(last_rows[2], last_rows[1], last_rows[0], predefined_list)
    else:
        desv = 100

    # Limpiar el bitmap combinado
    for y in range(24):
        for x in range(128):
            combined_bitmap[x, y] = 0

    # Llenar el bitmap combinado con los datos de las últimas tres filas
    for idx, r in enumerate(last_rows):
        if r is not None:
            for i in range(min(width, 32)):  # Ajustar para evitar desbordamiento
                if r[i * 2] == 124:  # "|"
                    val = 1  # Azul
                elif r[i * 2] == 78:  # "N"
                    val = 2  # Rojo
                else:
                    val = 0  # Negro
                
                for j in range(4):  # Ajustar escala a 4 pixeles
                    for k in range(2):  # Ajustar escala a 2 pixeles
                        x_pos = i * 3 + k
                        y_pos = idx * 4 + j
                        if x_pos < 128 and y_pos < 24:  # Asegurarse de no desbordar
                            combined_bitmap[x_pos, y_pos] = val

    text = ""
    for j in range(cam.height-3, cam.height):
        for i in range(cam.width):
            row[i * 2] = row[i * 2 + 1] = chars[
                buf[2 * (width * j + i)] * (len(chars) - 1) // 255
            ]
        text += row.decode() + "\n"
    
    msg = str(int(desv))
    if msg:
        data = msg.encode('utf-8')
        transmit_uart(data)
    
    update_display("desv:" + msg)
    time.sleep(0.1)  # Agregar un pequeño retraso para permitir que la UART procese la transmisión