from pathlib import Path

import pytest

from ar import Archive, ArchiveError


BAD_ARCHIVE = Path('test_data/bad.a')


def test_bad_file():
    with BAD_ARCHIVE.open('rt') as f:
        with pytest.raises(ArchiveError) as exception_info:
            Archive(f)
        assert str(exception_info.value) == "Stream must be binary"
