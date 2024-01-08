
import socket
import pickle
import threading
import multiprocessing
import timeit


SERVER = socket.gethostbyname(socket.gethostname())
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
            graph, start_node, num_processes = pickle.loads(data)
            result = parallel_bfs(graph, start_node)
            result = result_to_string(result)
            singular_execution_time = timeit.timeit(lambda: parallel_bfs(graph, start_node, 1), number = 1)
            multi_process_execution_time = timeit.timeit(lambda: parallel_bfs(graph, start_node), number = 1)
            data = pickle.dumps((result, singular_execution_time, multi_process_execution_time))
            conn.send(data)

    print(f"Closing connection: {addr}")


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


def parallel_bfs(graph, start_node, num_processes = -1):
    if num_processes == -1:
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