import time
import threading

class Client:
    def __init__(self):
        self.running = True

    def run(self):
        index = 0
        while self.running:
            print(f'thread running {index}')
            index += 1
            time.sleep(5)
    
    def stop_thread(self):
        self.running = False
            
if __name__ == "__main__":
    client = Client()
    t1 = threading.Thread(target = client.run, daemon=True)
    t1.start()

    while True:
        inp = input("Put input:")
        if inp == "quit":
            client.stop_thread()
            break