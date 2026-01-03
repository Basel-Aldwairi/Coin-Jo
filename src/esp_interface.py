# Basel Al-Dwairi - Interface for ESP & ESPCAM
# Socket Programming

import socket
import struct
import coin_model
import cv2


# IPs and ports that are used
LAPTOP_IP = "0.0.0.0"
TRIGGER_PORT = 6000  # ESP
CAMERA_PORT = 7000 # ESPCAM
CAMERA_IP = "192.168.1.49"

# Classification Model
model = coin_model.CoinModel()

# Map to turn output of mode.predict_image to sendable int
label_map = {
    '0.5 JD' : 0,
    '0.25 JD' : 1,
    '10 Piasters' : 2,
    '5 Piasters' : 3,
}

# Computer Server to handle connections from ESP
trigger_server = socket.socket()
trigger_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
trigger_server.settimeout(10)
trigger_server.bind((LAPTOP_IP, TRIGGER_PORT))
trigger_server.listen(1)


conn, _ = trigger_server.accept()
conn.settimeout(10)
# While ESP is connected
while conn:

    print("Waiting for ESP32 trigger...")

    msg = conn.recv(1024).decode().strip()

    if msg == '':
        print("Closed Connection")
        conn.close()
        break

    if msg != "TAKE_PIC":
        print("Invalid trigger")
        continue

    print("Trigger received")


    # Connect to ESPCAM server to send a trigger to take picture
    cmd = socket.socket()
    cmd.connect((CAMERA_IP, CAMERA_PORT))
    cmd.settimeout(10)
    cmd.sendall(b'\x01') # Trigger is 0x01


    # Read size to continue to read Image
    raw_size = cmd.recv(4)
    size = struct.unpack("<I", raw_size)[0]

    data = b""
    while len(data) < size:
        packet = cmd.recv(1024)
        if not packet:
            break
        data += packet


    # Save sent image
    with open("image.jpg", "wb") as f:
        f.write(data)

    print("Image saved successfully")

    # Open image with cv2
    img = cv2.imread("image.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Predict Class
    predictions = model.predict_image(img)

    predictions.sort(reverse=True)
    confidence, prediction = predictions[0]

    # Send prediction to ESP
    label = label_map[prediction]
    packed_data = struct.pack('!i', label)
    conn.sendall(packed_data)

    cmd.close()


print('ESP Closed')
trigger_server.close()
