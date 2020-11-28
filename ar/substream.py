import io

class Substream(io.RawIOBase):
    def __init__(self, file: io.RawIOBase, start, size):
        self.file = file
        self.start = start
        self.size = size
        self.p = 0
    
    def seek(self, offset, origin=0):
        #print('seeking to: {}'.format(offset))
        if origin == 0:
            self.p = offset
        elif origin == 1:
            self.p += offset
        # TODO: origin == 2
        else:
            raise ValueError("Unexpected origin: {}".format(origin))

    def read(self, n):
        #print('read {}'.format(n))
        prev = self.file.tell()
        self.file.seek(self.start + self.p)
        data = self.file.read(n if self.p + n <= self.size else self.size - self.p)
        self.p += len(data)
        self.file.seek(prev)
        return data

    def close(self):
        #print('closing')
        pass