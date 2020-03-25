import threading
import time


class CMultiThread(threading.Thread):
    def __init__(self, threaID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threaID
        self.name = name
        self.counter = counter
    
    def run(self):
        self.PrintString(self.name, 2, self.counter)
    
    @staticmethod
    def PrintString(name, delay, counter):
        while counter:
            time.sleep(delay)
            print('............%s:%s' % (name, time.ctime(time.time())))
            counter -= 1


if __name__ == '__main__':
    thread1 = CMultiThread(1, "thread11", 5)
    thread1.start()
