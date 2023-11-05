[![Build Status](https://travis-ci.com/vidstige/ar.svg?branch=master)](https://travis-ci.com/vidstige/ar)

![python-3.11](https://img.shields.io/badge/python-3.11-success)
![python-3.10](https://img.shields.io/badge/python-3.10-success)
![python-3.9](https://img.shields.io/badge/python-3.9-success)
![python-3.8](https://img.shields.io/badge/python-3.8-success)
![python-3.7](https://img.shields.io/badge/python-3.7-success)
![python-3.6](https://img.shields.io/badge/python-3.6-success)
![python-3.5](https://img.shields.io/badge/python-3.5-success)

# ar
Python package for parsing ar archive file. 

## Installation
`pip install ar`

## Usage
List files inside `file.a`:

```python
with open('file.a', "rb") as f:
    archive = Archive(f)
    for entry in archive:
        print(entry.name)
```

Read content of `file.txt` contained within `file.a`:

```python
with open('file.a', "rb") as f:
    archive = Archive(f)
    print(archive.open('file.txt').read())
```

Save each object files:

```python
with open('file.a', "rb") as f:
    archive = Archive(f)
    for entry in archive:
        fout = open(entry.name, "wb")
        fin = open(filepath, "rb")
        fin.seek(entry.offset)
        buffer = fin.read(entry.size)
        fout.write(buffer)
        fout.close()
```

## Author
- [Samuel Carlsson](https://github.com/vidstige)

## Contributors
- [Zhuo Zhang](https://github.com/zchrissirhcz)
