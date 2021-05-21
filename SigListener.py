from multiprocessing.connection import Listener
import threading
from _thread import interrupt_main


class SigListener:
    def __init__(self, port):
        self.listenerThread = threading.Thread(target=self.listen)
        self.port = port

    def start(self):
        self.listenerThread.start()

    def listen(self):
        address = ('localhost', self.port)
        listener = Listener(address, authkey=b'12321')

        while True:
            conn = listener.accept()
            msg = conn.recv()
            if msg.strip() == 'TERMINATE':
                conn.close()
                break
        listener.close()
        interrupt_main()  # raises keyboard interrupt in main thread
