
import socket
import threading
import pickle

SERVER = 'localhost'
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = ('utf-8')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def start():
    server.listen()
    print(f"Server is listening on {SERVER}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")


def handle_client(conn, addr):
    print(f"New connection: {addr}")

    connected = True
    while connected:
        data = conn.recv(4096)
        if not data:
            connected = False
        else:
            graph, start_node = pickle.loads(data)
            result = parallel_bfs(graph, start_node)
            result = pickle.dumps(result)
            conn.send(result)

    print(f"Closing connection: {addr}")


def parallel_bfs(graph, start_node):
    return "Traversed graph"

print("Server is starting...")
start()