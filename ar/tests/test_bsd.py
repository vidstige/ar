# pylint: disable=redefined-outer-name
import subprocess
from pathlib import Path

from ar import Archive, ArchiveError


ARCHIVE = Path('test_data/bsd.a')


def test_list():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        actual = [entry.name for entry in archive]
        expected = ['file0.txt', 'file1.bin', 'long-filename.txt']
        assert expected == actual


def test_read_content():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.read(1) == 'H'
        assert file0.read() == 'ello'


def test_read_content_long_filename():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('long-filename.txt')
        assert file0.read(1) == 'l'
        assert file0.read() == 'ong filename\n'

def test_read_binary():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file1.bin', 'rb')
        assert file0.read() == b'\xc3\x28'


def test_seek_basic():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.seek(1) == 1
        assert file0.read(3) == 'ell'
