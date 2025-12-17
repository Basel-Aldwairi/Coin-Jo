import socket


ip_address = '0.0.0.0'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_address, port))
server.listen()

print('/Waiting ...')

conn, addr =server.accept()

print('Connected by', addr)

i = 5

print('hello'.encode())

while True:
    data = conn.recv(1024)

    i -= 1
    if not data:
        break

    message = data.decode()
    print('recieved : ', message)

    reply = 'all good'.encode()
    if i <= 0:
        conn.sendall('\0'.encode())

    else:
        conn.sendall(reply)

conn.close()