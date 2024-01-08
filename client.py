
import socket
import pickle


SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

graph = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F', 'G'], 'D': [], 'E': [], 'F': [], 'G': [] }
start_node = 'A'

num_processes = int(input("Please enter number of processes: "))

data = pickle.dumps((graph, start_node, num_processes))
client.send(data)

data = client.recv(4096)
result, singular_execution_time, multi_process_execution_time = pickle.loads(data)

print(f"Result: \n {result}")
print(f"Single process execution time: {singular_execution_time}")
print(f"Multi process execution time: {multi_process_execution_time}")


