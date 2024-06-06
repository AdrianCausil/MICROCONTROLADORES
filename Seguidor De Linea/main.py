import network, socket,time
from machine import Timer,Pin,PWM,UART
from L298N_motor import L298N
from Matrix import Matrix
import array
import random
uart = UART(0,baudrate=115200,bits=8,parity=None,stop=1,rx=Pin(17),tx=Pin(16))
ENA = PWM(Pin(0))
IN1 = Pin(1, Pin.OUT)
IN2 = Pin(2, Pin.OUT)
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ENB = PWM(Pin(5))
SWITCH_PIN = 27
switch_pin = Pin(SWITCH_PIN, Pin.IN, Pin.PULL_UP)
motor1 = L298N(ENA, IN1, IN2)  # create a motor1 object
motor2 = L298N(ENB, IN3, IN4)  # create a motor2 object

class Perceptron:
    def __init__(self, name_or_input_size, output_size=None):
        if isinstance(name_or_input_size,str):
            self.weights = Matrix.load_file(name_or_input_size)
        else:
            self.weights = Matrix(name_or_input_size+1, output_size+1,  [random.random() for _ in range((name_or_input_size+1) * (output_size+1))])  

    def predict(self, inputs):
        tail=False
        if inputs.n==self.weights.m-1:
            result = Matrix.untail(Matrix.tail(inputs) * self.weights)
        else:
            result = inputs * self.weights
        return result

    def train(self, inputs, labels, learning_rate=0.01, epochs=1):
        if inputs.n==self.weights.m-1:
            inputs=Matrix.tail(inputs)
        if labels.n==self.weights.n-1:
            labels=Matrix.tail(labels)
        for epoch in range(epochs):
            predictions = self.predict(inputs)
            
            error = labels - predictions
            self.weights=self.weights.add_tail(  inputs.T() * error * learning_rate)

            
    def save_file(self,name):
        self.weights.save_file(name)

# Example usage
if __name__ == "__main__":
    val=""
    datoant= None
    
    perceptron = Perceptron(name_or_input_size=1, output_size=2)

            
    def load():
            global perceptron
            perceptron = Perceptron("m.txt") 
            
    def train_control():
          global cont_train,repeat,val
          if repeat:
            dat = int(val)
            dat1 =int(val)/100
            floor_colors = Matrix(1,1,[dat1])
            if train:
                global datoant
                stop_timer = Timer(-1)

                def stop_motors():
                    motor1.stop()
                    motor2.stop()

                # Detener el temporizador si está activo
                stop_timer.deinit()
                datant=0

                if dat == -datant:
                    return
                else:
                    datant=dat
                    if -30 <= dat <= 30:
                        motor1.setSpeed(59000)
                        motor2.setSpeed(56000)
                        v_i=(59000/65000)
                        v_d=(56000/65000)
                        motors_vel= Matrix(1,2,[v_i,v_d])
                        #perceptron.train(floor_colors, motors_vel)
                        #perceptron.save_file("m.txt")
                        motor1.forward()
                        motor2.forward()
                        stop_timer.init(period=35, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())  
                    elif -55 <= dat < -30:
                        motor1.setSpeed(61000)
                        motor2.setSpeed(45000)
                        v_i=(61000/65000)
                        v_d=(45000/65000)
                        motors_vel= Matrix(1,2,[v_i,v_d])
                        #perceptron.train(floor_colors, motors_vel)
                        #perceptron.save_file("m.txt")
                        motor1.forward()
                        motor2.forward()
                        stop_timer.init(period=27, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())  
                        
                    elif dat < -55:
                        motor1.setSpeed(65000)
                        motor2.setSpeed(45000)
                        v_i=(65000/65000)
                        v_d=(45000/65000)
                        
                        motors_vel= Matrix(1,2,[v_i,v_d])
                        #perceptron.train(floor_colors, motors_vel)
                        #perceptron.save_file("m.txt")
                        motor1.forward()
                        motor2.forward()
                        stop_timer.init(period=27, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())  
                    elif 30 < dat <= 62:
                        motor1.setSpeed(46000)
                        motor2.setSpeed(55000)
                        v_i=(46000/65000)
                        v_d=(55000/65000)
                        motors_vel= Matrix(1,2,[v_i,v_d])
                        #perceptron.train(floor_colors, motors_vel)
                        #perceptron.save_file("m.txt")
                        motor1.forward()
                        motor2.forward()
                        stop_timer.init(period=25, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())  
                    elif dat > 62:
                        motor1.setSpeed(46000)
                        motor2.setSpeed(59000)
                        v_i=(46000/65000)
                        v_d=(59000/65000)
                        motors_vel= Matrix(1,2,[v_i,v_d])
                        #perceptron.train(floor_colors, motors_vel) 
                        #perceptron.save_file("m.txt")
                        motor1.forward()
                        motor2.forward()
                        stop_timer.init(period=25, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())        
            else:
                stop_timer = Timer(-1)
                
                stop_timer.deinit()
                
                def stop_motors():
                    motor1.stop()
                    motor2.stop()
                    
                prediction=perceptron.predict(floor_colors)
                v_i = prediction[0,0]
                v_d = prediction[0,1]
                print(v_i,v_d)
                m1=abs(int(v_i*65000))
                m2=abs(int(v_d*65000))
                motor1.setSpeed(m1)
                motor2.setSpeed(m2)
                motor1.forward()
                motor2.forward()
                stop_timer.init(period=34, mode=Timer.ONE_SHOT, callback=lambda t: stop_motors())
                #print('predic', prediction)
    while True:
        repeat=True
        if uart.any():
            rd = uart.read(3)
            if rd != None:
                val = int(rd.decode('utf-8','replace'))

                if switch_pin.value() == 0:  # Switch active (pulled down)
                    train=True

                else:  # Switch inactive (pulled up)
                    train=False
                    load()
                    
                train_control()