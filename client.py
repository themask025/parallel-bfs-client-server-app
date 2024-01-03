
import socket
import pickle

SERVER = 'localhost'
PORT = 5050
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


graph = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F', 'G'], 'D': [], 'E': [], 'F': [], 'G': [] }
start_node = 'A'

data = pickle.dumps((graph, start_node))
client.send(data)

result = pickle.loads(client.recv(4096))
print(result)


