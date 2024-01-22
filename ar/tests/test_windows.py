# pylint: disable=redefined-outer-name
import subprocess
from pathlib import Path

import pytest

from ar import Archive, ArchiveError


ARCHIVE = Path('test_data/MiniLib.lib')


def test_list():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        expected = ['x64\\Release\\pch.ob', 'x64\\Release\\MiniLib.ob']
        actual = [entry.name for entry in archive]
        assert actual == expected


def test_read_binary():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('x64\\Release\\MiniLib.ob', 'rb')
        assert file0.read(16) == b'\x00\x00\xff\xff\x01\x00d\x86tF\xaee8\xfe\xb3\x0c'


def test_seek_basic():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('x64\\Release\\MiniLib.ob', 'rb')
        file0.seek(1)
        assert file0.read(3) == b'\x00\xff\xff'


def test_tell():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('x64\\Release\\MiniLib.ob', 'rb')
        assert file0.tell() == 0
        file0.read(2)
        assert file0.tell() == 2
        file0.read()
        assert file0.tell() == 1887


def test_open_missing_path():
    with ARCHIVE.open('rb') as f:
        archive = Archive(f)
        with pytest.raises(ArchiveError) as exception_info:
            archive.open('missing')
        assert str(exception_info.value) == "No such entry: missing"
