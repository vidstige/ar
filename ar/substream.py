import io

class Substream(io.RawIOBase):
    def __init__(self, file: io.RawIOBase, start, size):
        super().__init__()
        self.file = file
        self.start = start
        self.size = size
        self.position = 0

    def seek(self, offset, origin=0):
        if origin == 0:
            self.position = offset
        elif origin == 1:
            self.position += offset
        elif origin == 2:
            self.position = self.size + offset
        else:
            raise ValueError("Unexpected origin: {}".format(origin))

    def read(self, n=None):
        if n is None:
            n = self.size
        prev = self.file.tell()
        self.file.seek(self.start + self.position)
        data = self.file.read(n if self.position + n <= self.size else self.size - self.position)
        self.position += len(data)
        self.file.seek(prev)
        return data

    def close(self):
        pass
