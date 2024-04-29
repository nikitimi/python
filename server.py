import socket
import threading
from multiprocessing import Process

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((SERVER_HOST, SERVER_PORT))
        self.clients:list[threading.Thread] = []

    def start(self):
        self.socket.listen(5)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"New connection from {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
            self.clients.append(client_handler)

    def handle_client(self, client_socket:socket.socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    print(f"Received from client: {data.decode()}")
                    self.broadcast(data)
                else:
                    self.remove_client(client_socket)
                    break
            except Exception as e:
                print(f"Error handling client: {e}")
                self.remove_client(client_socket)
                break

    def broadcast(self, data:bytes):
        for client in self.clients:
            if client.is_alive():
                print(data)
                # client._target(data)

    def remove_client(self, client_socket:socket.socket):
        if client_socket in self.clients:
            client_socket.join()
            self.clients.remove(client_socket)
            print("Client disconnected")

def main():
    server = Server()
    server_thread = Process(target=server.start)
    server_thread.start()

if __name__ == "__main__":
    main()
