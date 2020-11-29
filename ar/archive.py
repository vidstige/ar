"""Loads AR files"""
import struct
from ar.substream import Substream

MAGIC = b"!<arch>\n"


def padding(n, pad_size):
    reminder = n % pad_size
    if reminder:
        return pad_size - n % pad_size
    return 0


def pad(n, pad_size):
    return n + padding(n, pad_size)


class ArchiveError(Exception):
    pass


class ArPath:
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size

    def get_stream(self, f):
        return Substream(f, self.offset, self.size)


class Archive:
    def __init__(self, f):
        self.f = f
        self.entries = list(load(self.f))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return iter(self.entries)

    def open(self, path):
        arpath = path
        if not isinstance(arpath, ArPath):
            arpath = next((entry for entry in self.entries if entry.name == arpath), None)
            if arpath is None:
                raise ArchiveError('No such entry: {}'.format(arpath))
        return arpath.get_stream(self.f)


def lookup(data, offset):
    start = offset
    end = data.index(b"\n", start)
    return data[start:end - 1].decode()


def load(stream):
    actual = stream.read(len(MAGIC))
    if actual != MAGIC:
        raise ArchiveError("Unexpected magic: '{magic}'".format(magic=actual))

    fmt = '16s12s6s6s8s10sbb'

    lookup_data = None
    while True:
        buffer = stream.read(struct.calcsize(fmt))
        if len(buffer) < struct.calcsize(fmt):
            break
        name, timestamp, owner, group, mode, size, _, _ = struct.unpack(fmt, buffer)
        del timestamp, owner, group, mode
        name = name.decode().rstrip()
        size = int(size.decode().rstrip())

        if name == '/':
            stream.seek(pad(size, 2), 1)
        elif name == '//':
            # load the lookup
            lookup_data = stream.read(size)
            stream.seek(padding(size, 2), 1)
        elif name.startswith('/'):
            lookup_offset = int(name[1:])
            expanded_name = lookup(lookup_data, lookup_offset)
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            yield ArPath(expanded_name, offset, size)
        else:
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            yield ArPath(name.rstrip('/'), offset, size)
