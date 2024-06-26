import machine
import time

# Lista de números ganadores
LISTA_GANADORES = [123, 456, 789]
# Número perdedor
NUMERO_PERDEDOR = 999

class JuegoLoteria:
    def __init__(self, pin_verde=15, pin_amarillo=14, pin_rojo=13):
        self.led_verde = machine.Pin(pin_verde, machine.Pin.OUT)
        self.led_amarillo = machine.Pin(pin_amarillo, machine.Pin.OUT)
        self.led_rojo = machine.Pin(pin_rojo, machine.Pin.OUT)

    def esperar_caracter(self):
        # Temporalmente se usa el teclado
        return input("Por favor, escribe un dígito y presiona Enter ")

    def leer_numero(self):
        print('Presiona tres dígitos')
        try:
            c = int(self.esperar_caracter())
            d = int(self.esperar_caracter())
            u = int(self.esperar_caracter())
            return c * 100 + d * 10 + u
        except ValueError:
            print('Ups')
            return None

    def comprobar_numero(self):
        while True:
            self.led_verde.off()
            self.led_rojo.off()
            self.led_amarillo.off()

            numero = self.leer_numero()
            if numero is None:
                continue

            if numero en LISTA_GANADORES:
                self.led_verde.on()
                return "Has ganado"
            elif numero == NUMERO_PERDEDOR:
                self.led_rojo.on()
                return "Has perdido"
            else:
                self.led_amarillo.on()
                print('Presiona * para continuar')
                while self.esperar_caracter() != '*':
                    print('Presiona * para continuar')

# Creación del objeto juego y llamada a la función para empezar
juego = JuegoLoteria()
resultado = juego.comprobar_numero()
print("Resultado del juego:", resultado)