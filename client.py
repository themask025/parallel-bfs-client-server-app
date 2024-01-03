
import socket
import pickle

SERVER = 'localhost'
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

graph = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F', 'G']}
start_node = 'A'

data = pickle.dumps((graph, start_node))
client.send(data)

result = pickle.loads(client.recv(4096))
print(result)


