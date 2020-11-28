"""Loads AR files"""
import struct
from pyar.substream import Substream

magic = b"!<arch>\n"


def padding(n, pad_size):
    reminder = n % pad_size
    if reminder:
        return pad_size - n % pad_size
    return 0


def pad(n, pad_size):
    return n + padding(n, pad_size)


class ArchiveError(Exception):
    pass


class Entry(object):
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size

    def get_stream(self, f):
        return Substream(f, self.offset, self.size)
   

class Archive(object):
    def __init__(self, entries):
        self.entries = entries


def lookup(data, offset):
    start = offset
    end = data.index(b"\n", start)
    return data[start:end-1].decode()


def load(stream):
    actual = stream.read(len(magic))
    if actual != magic:
        raise ArchiveError("Unexpected magic")

    fmt = '16s12s6s6s8s10sbb'

    lookup_data = None
    entries = []
    while True:
        buffer = stream.read(struct.calcsize(fmt))
        if len(buffer) < struct.calcsize(fmt):
            break
        name, timestamp, owner, group, mode, size, _, _ =  struct.unpack(fmt, buffer)
        name = name.decode().rstrip()
        size = int(size.decode().rstrip())
        #print("'{}': {} ({})".format(name, size, pad(size, 2)))

        if name == '/':
            stream.seek(pad(size, 2), 1)
        elif name == '//':
            # load the lookup
            lookup_data = stream.read(size)
            stream.seek(padding(size, 2), 1)
        elif name.startswith('/'):
            o = int(name[1:])
            expanded_name = lookup(lookup_data, o)
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            entries.append(Entry(expanded_name, offset, size))
        else:
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            entries.append(Entry(name.rstrip('/'), offset, size))

    return Archive(entries)
