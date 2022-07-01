import datetime
import os

class text_writer:

    def open(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def close(self):
        raise NotImplementedError()

    def write(self, text: str):
        raise NotImplementedError()