import picar_4wd as fc
import sys
import tty
import termios
import asyncio
import socket
import subprocess
import os
import time
import struct

HOST = "192.168.88.17" # IP address of your Raspberry PI
PORT = 65437          # Port to listen on (non-privileged ports are > 1023)

def power_read():
    from picar_4wd.adc import ADC
    power_read_pin = ADC('A4')
    power_val = power_read_pin.read()
    power_val = power_val / 4095.0 * 3.3
    print(power_val)
    power_val = power_val * 3
    power_val = round(power_val, 2)
    print(power_val)
    return power_val

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    spd = 30
    try:
        while True:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            for char in data:
                print(char)
            if data != b"":
                print(data)     
                if 119 in data:           # If w (ASCII val = 102) in data  
                    print("forward")
                    fc.forward(spd)
                    client.sendall(data) # Echo back to client
                elif 115 in data:         # If s (ASCII val = 98) in data
                    print("backward")
                    fc.backward(spd)
                    client.sendall(data) # Echo back to client
                elif 97 in data:          # If a (ASCII val = 76) in data
                    print("left")
                    fc.turn_left(spd)
                    client.sendall(data) # Echo back to client
                elif 100 in data:         # If d (ASCII val = 82) in data
                    print("right")
                    fc.turn_right(spd)
                    client.sendall(data) # Echo back to client
                elif 113 in data:
                    print("stop")
                    fc.stop() 
                elif 101 in data:
                    pwr = power_read()
                    print("check1")
                    pwr_f = struct.pack('!f', pwr)
                    print(pwr)
                    data = pwr_f
                    print(data)
                    client.sendall(data)
                elif 60 in data:
                    spd = spd - 1
                    print("decreasing speed", spd)
                    client.sendall(data) # Echo back to client
                elif 62 in data:
                    spd = spd + 1
                    print("increasing speed", spd)  
                    client.sendall(data) # Echo back to client

            
    except:
        print("exception")
