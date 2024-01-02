# # echo client

# # 2 - Client initiates a connection

# import socket

# HOST = "localhost"
# PORT = 12345

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))

# # 3 - Data is exchanged

#     s.sendall(b"Hello, world")
#     data = s.recv(1024)

# print(f"Received {data}")

import socket

HEADER = 16
PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print("Message sent!")
    print(client.recv(2048).decode(FORMAT))

send("Hello world!")
input()
send("Hello everyone!")
input()
send("Hello user!")
input()

send(DISCONNECT_MESSAGE)