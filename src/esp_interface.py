import socket
import struct

LAPTOP_IP = "0.0.0.0"
TRIGGER_PORT = 6000
CAMERA_PORT = 7000
IMAGE_PORT = 8000
CAMERA_IP = "192.168.1.29"  # ESP32-CAM IP

# ---------- Trigger server ----------
trigger_server = socket.socket()
trigger_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
trigger_server.bind((LAPTOP_IP, TRIGGER_PORT))
trigger_server.listen(1)

# ---------- Image server ----------
img_server = socket.socket()
img_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
img_server.bind((LAPTOP_IP, IMAGE_PORT))
img_server.listen(1)

print("Waiting for ESP32 trigger...")

# ---- Receive trigger ----
conn, _ = trigger_server.accept()
msg = conn.recv(1024).decode().strip()
conn.close()

if msg != "TAKE_PIC":
    print("Invalid trigger")
    exit()

print("Trigger received")

# ---- Tell camera to take picture ----
cmd = socket.socket()
cmd.connect((CAMERA_IP, CAMERA_PORT))
cmd.send(b'\x01')
cmd.close()

print("Waiting for image...")

# ---- Receive image ----
conn, _ = img_server.accept()

raw_size = conn.recv(4)
size = struct.unpack("<I", raw_size)[0]

data = b""
while len(data) < size:
    packet = conn.recv(1024)
    if not packet:
        break
    data += packet

with open("image.jpg", "wb") as f:
    f.write(data)

conn.close()
print("Image saved successfully")