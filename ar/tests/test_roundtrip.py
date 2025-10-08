# pylint: disable=redefined-outer-name
import subprocess
import tempfile
from pathlib import Path

import pytest

from ar import Archive, ArchiveError


TEST_DATA = Path('test_data/')


@pytest.fixture
def simple_archive():
    archive_path = TEST_DATA / 'test.a'
    if archive_path.exists():
        return archive_path

    archive_full_path = archive_path.resolve()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / 'file0.txt').write_text('Hello')
        (tmp_path / 'file1.bin').write_bytes(b'\xc3\x28')  # invalid utf-8 characters
        (tmp_path / 'long_file_name_test0.txt').write_text('Hello2')
        (tmp_path / 'long_file_name_test1.bin').write_bytes(b'\xc3\x28')
        subprocess.check_call(
            ['ar', 'r', str(archive_full_path), 'file0.txt', 'file1.bin', 'long_file_name_test0.txt', 'long_file_name_test1.bin'],
            cwd=tmpdir,
        )

    return archive_path


def test_list(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        assert ['file0.txt', 'file1.bin', 'long_file_name_test0.txt', 'long_file_name_test1.bin'] == [entry.name for entry in archive]


def test_read_content(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.read(1) == 'H'
        assert file0.read() == 'ello'


def test_read_binary(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file1.bin', 'rb')
        assert file0.read() == b'\xc3\x28'

def test_read_content_ext(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('long_file_name_test0.txt')
        assert file0.read(2) == 'He'
        assert file0.read() == 'llo2'


def test_read_binary_ext(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('long_file_name_test1.bin', 'rb')
        assert file0.read() == b'\xc3\x28'


def test_seek_basic(simple_archive):
    with simple_archive.open('rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        file0.seek(1)
        assert file0.read(3) == 'ell'
