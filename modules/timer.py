from time import sleep

class Timer:
    seconds = 0

    def timer(self):
        global is_finish
        while not is_finish:
            self.seconds += 1
            sleep(1)