# pylint: disable=redefined-outer-name
from pathlib import Path

from ar import Archive


ARCHIVE = Path('test_data/linux.a')


def test_seekable():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt', 'r')
        assert file0.seekable()


def test_seek_from_start():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt', 'r')
        file0.seek(2)
        assert file0.tell() == 2
        assert file0.read(1) == 'l'


def test_seek_from_current():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt', 'r')
        assert file0.read(1) == 'H'
        file0.seek(1, 1)
        assert file0.tell() == 2
        assert file0.read(2) == 'll'


def test_seek_from_end():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt', 'r')
        file_size = 5
        file0.seek(-2, 2)
        assert file0.tell() == file_size - 2
        assert file0.read() == 'lo'
