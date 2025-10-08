import errno
import io

class Substream(io.RawIOBase):
    def __init__(self, file: io.RawIOBase, start: int, size: int):
        super().__init__()
        self.file = file
        self.start = start
        self.size = size
        self.position = 0

    def seek(self, offset, origin=0) -> int:
        if origin == 0:
            position = offset
        elif origin == 1:
            position = self.position + offset
        elif origin == 2:
            position = self.size + offset
        else:
            raise ValueError(f"Unexpected origin: {origin}")

        if position < 0 or position > self.size:
            raise OSError(errno.EINVAL, "Invalid argument")

        self.position = position
        return self.position

    def seekable(self):
        return True

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

    def tell(self) -> int:
        return self.position
