import threading


class BaseThreading(threading.Thread):
    def __init__(self, thread_name, func):
        self.thread_name = str(thread_name)
        self.func = func
        threading.Thread.__init__(self)
    
    def __str__(self):
        return self.thread_name
    
    def run(self):
        # print(self.thread_name, "スレッド")
        self.func()