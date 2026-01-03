import socket
import struct

laptop_ip = '192.168.1.49'
port = 6000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((laptop_ip, port))

while True:

    msg = b'TAKE_PIC'

    dec = input('press enter to send, q to quit : ')

    if dec == 'q':
        break
    socket.sendall(msg)


socket.close()