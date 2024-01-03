
import socket
import pickle
import threading
import multiprocessing


SERVER = 'localhost'
PORT = 5050
ADDR = (SERVER, PORT)

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
            result = result_to_string(result)
            result = pickle.dumps(result)
            conn.send(result)

    print(f"Closing connection: {addr}")


def singular_bfs(graph, start_node):
    visited = set()
    queue = [start_node]
    result = []

    while queue:
        current_node = queue.pop(0)
        if current_node not in visited:
            visited.add(current_node)
            result.append(current_node)
            queue.extend(graph[current_node])

    return result


def bfs(graph, start, visited, result_queue):
    queue = [start]

    while queue:
        current_node = queue.pop(0)

        if current_node not in visited:
            visited.append(current_node)

            result_queue.put(current_node)

            neighbors = graph[current_node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)


def parallel_bfs(graph, start_node):
    num_processes = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()

    visited = manager.list()
    result_queue = manager.Queue()
    processes = []

    for _ in range(num_processes):
        process = multiprocessing.Process(target=bfs, args=(graph, start_node, visited, result_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results


def result_to_string(result_list):
    return " -> ".join(map(str, result_list))



print("Server is starting...")
start()