import socket
import RPi.GPIO as GPIO
import time
steer_1 = 24 # pin 7
steer_2 = 23 # pin 5
enA = 25 # pin 3

GPIO.setmode(GPIO.BCM)

pins = [enA,steer_1,steer_2]

for element in pins:
GPIO.setup(element,GPIO.OUT) # to set up all GPIO pins
if element != enA:
GPIO.output(element,GPIO.LOW) # to set all drive pins low

steer=GPIO.PWM(enA,1000) # '1000' hertz duty cycle
steer.start(100)


mediapipeRe_socket = socket.socket()
mediapipeRe_socket.bind(('127.0.0.1', 11312))
mediapipeRe_socket.listen(1)

try:
    while True:
        print("Waiting for a connection...")
        client_socket, client_address = mediapipeRe_socket.accept()
        print(f"Accepted connection from {client_address}")

        while True:
            received_data = client_socket.recv(1024).decode()
            if not received_data:
                break
            print(received_data)
           
            try:
                if received_data == "opened":
                    GPIO.output(steer_1,GPIO.HIGH) # opens the door
                    GPIO.output(steer_2,GPIO.LOW)
                elif received_data == "clenched":
                   GPIO.output(steer_1,GPIO.LOW) # closes the door
                   GPIO.output(steer_2,GPIO.HIGH)
                elif received_data == "neither": # leaves the door where it is
                   GPIO.output(steer_1,GPIO.LOW)
                   GPIO.output(steer_2,GPIO.LOW)
                else:
                    print("Invalid command")
                 
            except Exception as e:
                print(f"Error: {e}")

        print(f"Connection closed")
        client_socket.close()

finally:
    GPIO.cleanup()
    mediapipeRe_socket.close()
