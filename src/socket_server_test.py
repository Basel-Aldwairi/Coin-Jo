import socket


ip_address = '0.0.0.0'
port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_address, port))
server.listen(1)

print('/Waiting ...')

conn, addr =server.accept()

print('Connected by', addr)

while True:
    data = conn.recv(1024)

    if not data:
        break

    message = data.decode()
    print('recieved : ', message)

    conn.sendall('all good'.encode())

conn.close()