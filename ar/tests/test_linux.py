# pylint: disable=redefined-outer-name
import subprocess
from pathlib import Path

import pytest

from ar import Archive, ArchiveError


ARCHIVE = Path('test_data/linux.a')


def test_list():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        assert ['file0.txt', 'file1.bin'] == [entry.name for entry in archive]


def test_read_content():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.read(1) == 'H'
        assert file0.read() == 'ello'


def test_read_binary():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file1.bin', 'rb')
        assert file0.read() == b'\xc3\x28'


def test_seek_basic():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        file0.seek(1)
        assert file0.read(3) == 'ell'


def test_open_missing_path():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        with pytest.raises(ArchiveError) as exception_info:
            archive.open('missing')
        assert str(exception_info.value) == "No such entry: missing"
