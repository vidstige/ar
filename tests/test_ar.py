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


def test_open_file_list(simple_archive):
    with open(simple_archive, 'rb') as f:
        archive = Archive(f)
        assert ['file0.txt', 'file1.txt'] == [entry.name for entry in archive]


def test_open_file_read_content(simple_archive):
    with open(simple_archive, 'rb') as f:
        archive = Archive(f)
        file0 = archive.open('file0.txt')
        assert file0.read(1) == b'H'
        assert file0.read() == b'ello'
