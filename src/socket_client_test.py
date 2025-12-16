import socket

server_ip = '192.168.1.49'
port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))


while True:
    message = input('Enter message : ')

    if message == 'quit':
        break

    client.sendall(message.encode())
    print('sent message : ', message)

    reply = client.recv(1024)
    print('replied with : ', reply.decode())

client.close()