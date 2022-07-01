from threading import Lock, Thread
from typing import List


class thread_waiter:

    __threads: List[Thread]
    __mutex: Lock

    def __init__(self):
        self.__threads = []
        self.__mutex = Lock()
    
    def add(self, thread: Thread):
        self.__mutex.acquire()

        self.__threads.append(thread)

        self.__mutex.release()

    def refresh(self):
        #self.__threads = [thread for thread in self.__threads if thread.is_alive()]
        if self.__mutex.locked():
            return
        self.__mutex.acquire()

        i = 0
        while i < len(self.__threads):
            thread = self.__threads[i]
            if not thread.is_alive():
                del self.__threads[i]
            else:
                i+=1

        self.__mutex.release()

    def wait(self):
        print(len(self.__threads))
        for thread in self.__threads:
            thread.join()
        
    
