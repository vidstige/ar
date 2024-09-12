"""Loads AR files"""
import struct
import codecs
from typing import BinaryIO, Iterable, Union

from ar.substream import Substream


MAGIC = b"!<arch>\n"


def padding(n: int, pad_size: int) -> int:
    reminder = n % pad_size
    return pad_size - reminder if reminder else 0


def pad(n: int, pad_size: int):
    return n + padding(n, pad_size)


class ArchiveError(Exception):
    pass


class ArPath:
    def __init__(self, name: str, offset: int, size: int):
        self.name = name
        self.offset = offset
        self.size = size

    def get_stream(self, f):
        return Substream(f, self.offset, self.size)


class Mode:
    MODES = 'rbt'
    def __init__(self, mode):
        if any(character not in Mode.MODES for character in mode):
            raise ValueError(f"invalid mode: '{mode}'")
        self._mode = mode

    def is_binary(self) -> bool:
        return 'b' in self._mode


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

    def open(self, path: Union[str, ArPath], mode='r', encoding='utf-8'):
        modef = Mode(mode)
        if isinstance(path, ArPath):
            arpath = path
        else:
            try:
                arpath = next(entry for entry in self.entries if entry.name == path)
            except StopIteration as e:
                raise ArchiveError(f'No such entry: {path}') from e

        binary = arpath.get_stream(self.f)
        if modef.is_binary():
            return binary
        return codecs.getreader(encoding)(binary)


def lookup(data: bytes, offset: int) -> str:
    for delim in (b"\x00", b"\x2F"):
        pos = data.find(delim, offset)
        if pos >= 0:
            data = data[offset:pos]
    return data.decode()


ENTRY_FORMAT = '16s12s6s6s8s10sbb'


def load(stream: BinaryIO) -> Iterable[ArPath]:
    magic = stream.read(len(MAGIC))
    if not isinstance(magic, bytes):
        raise ArchiveError("Stream must be binary")
    if magic != MAGIC:
        raise ArchiveError(f"Unexpected magic: {magic!r}")

    lookup_data = None
    while True:
        buffer = stream.read(struct.calcsize(ENTRY_FORMAT))
        if len(buffer) < struct.calcsize(ENTRY_FORMAT):
            break
        name, timestamp, owner, group, mode, size, _, _ = struct.unpack(ENTRY_FORMAT, buffer)
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
            if lookup_data is None:
                raise ArchiveError("GNU long filename not allowed before lookup table")
            expanded_name = lookup(lookup_data, lookup_offset)
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            yield ArPath(expanded_name, offset, size)
        elif name.startswith('#1/'):
            # BSD long filenames
            name_length = int(name[len('#1/'):])
            long_name = stream.read(name_length).rstrip(b'\00').decode()
            offset = stream.tell()
            stream.seek(pad(size - name_length, 2), 1)
            yield ArPath(long_name, offset, size - name_length)
        else:
            offset = stream.tell()
            stream.seek(pad(size, 2), 1)
            yield ArPath(name.rstrip('/'), offset, size)
