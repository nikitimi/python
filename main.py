from multiprocessing import Process

from modules.tkinter.client import Client
from modules.tkinter.server import Server

import threading

def initialize_client():
    global is_terminated
    client = Client()
    client_thread = threading.Thread(target=client.connect_to_server)
    client_thread.start()
    client.deiconify()
    # client.bind("<Destroy>", on_frame_destroy)
    client.mainloop()
    is_terminated = True

def initialize_server():
    server = Server()
    server_thread = Process(target=server.start)
    server_thread.start()

if __name__ == "__main__":
    print("Hello World")
    