# pylint: disable=redefined-outer-name
import subprocess
from pathlib import Path

import pytest

from ar import Archive, ArchiveError


TEST_DATA = Path('test_data/')


@pytest.fixture
def simple_archive():
    # Create archive
    TEST_DATA.mkdir(exist_ok=True)

    (TEST_DATA / 'file0.txt').write_text('Hello')
    (TEST_DATA / 'file1.txt').write_text('World')
    subprocess.check_call('ar r test.a file0.txt file1.txt'.split(), cwd=TEST_DATA)
    return TEST_DATA / 'test.a'

@pytest.fixture
def bad_archive():
    path = TEST_DATA / 'bad.a'
    path.write_bytes(b'nope, not an ar file')
    return path


def test_list(simple_archive):
    with open(simple_archive, 'rb') as f:
        archive = Archive(f)
        assert ['file0.txt', 'file1.txt'] == [entry.name for entry in archive]


def test_read_content(simple_archive):
    with open(simple_archive, 'rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.read(1) == 'H'
        assert file0.read() == 'ello'


def test_seek_basic(simple_archive):
    with open(simple_archive, 'rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        file0.seek(1)
        assert file0.read(3) == 'ell'


def test_bad_file(bad_archive):
    with bad_archive.open('rb') as f:
        with pytest.raises(ArchiveError) as exception_info:
            Archive(f)
        assert str(exception_info.value) == "Unexpected magic: b'nope, no'"
