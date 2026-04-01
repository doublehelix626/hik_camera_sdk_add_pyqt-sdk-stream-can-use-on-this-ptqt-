import threading
from queue import Queue
import cv2
from PyQt5.QtCore import QThread
from utils.QT_thread_pool import QT_ThreadPool

sleep = QThread.msleep


def read_stream(stream_obj, queue, interval):
    while True:
        ret, framer = stream_obj.read()
        if ret:
            if queue.full():
                queue.get()
            queue.put(framer)
        sleep(interval)


class _Stream:
    def __init__(self, stream_addr, fps=30, maxsize=5):
        self.queue = Queue(maxsize)
        self.fps = fps
        self.last_frame = None
        self.stream_obj = cv2.VideoCapture(stream_addr)
        if not self.stream_obj.isOpened():
            raise Exception(f"stream addr: {stream_addr} open failure")
        pool = QT_ThreadPool()
        pool.submit(f"open_stream({stream_addr})", read_stream, self.stream_obj, self.queue, int(fps/1000))

    def __next__(self):
        if self.queue.empty() and self.last_frame is None:
            return None
        if self.queue.empty() and self.last_frame is not None:
            return self.last_frame
        if not self.queue.empty():
            self.last_frame = self.queue.get()
            return self.last_frame

    def __iter__(self):
        return self

    def flask_stream(self):
        self.queue.clear()

    def get_last_frame(self):
        return self.last_frame


class StreamManager:
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.lock = threading.RLock()
            self.stream_dict = dict()
        self.__first_init = False

    def open_stream(self, stream_addr, fps=30, maxsize=5):
        with self.lock:
            if stream_addr not in self.stream_dict.keys():
                stream_obj = _Stream(stream_addr, fps=fps, maxsize=maxsize)
                self.stream_dict[stream_addr] = stream_obj
            else:
                stream_obj = self.stream_dict[stream_addr]
            return stream_obj


