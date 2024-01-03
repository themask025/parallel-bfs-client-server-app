
import socket
import pickle


HEADER = 16
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def send_graph(data):
    client.send(pickle.dumps(data))


def send(msg):
    message = msg.encode(FORMAT)

    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    client.send(message)
    print("Message sent!")


def start():
    print(f"Connecting to {ADDR} ...")
    client.connect(ADDR)
    print(client.recv(2048).decode(FORMAT))

    send("Hello world!")
    print(client.recv(2048).decode(FORMAT))

    send(DISCONNECT_MESSAGE)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

graph = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F', 'G']}
start_node = 'A'

print("[STARTING] client is starting...")
start()