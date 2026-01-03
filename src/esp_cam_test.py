import socket

laptop_ip = '192.168.1.49'
port = 7000

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((laptop_ip, port))
server.listen(1)

conn, _ = server.accept()


while True:

    msg = conn.recv(1024).decode().strip()
    print(msg)
    if msg == 'quit':
        break

conn.close()

