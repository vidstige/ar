[![Build Status](https://travis-ci.com/vidstige/ar.svg?branch=master)](https://travis-ci.com/vidstige/ar)

![python-3.8](https://img.shields.io/badge/python-3.8-success)
![python-3.7](https://img.shields.io/badge/python-3.7-success)
![python-3.6](https://img.shields.io/badge/python-3.7-success)
![python-3.5](https://img.shields.io/badge/python-3.5-success)

# ar
Python package for parsing ar archive file. 

## Installation
`pip install ar`

## Usage
List files inside `file.a`
```python
with open('file.a') as f:
  archive = Archive(f)
  for entry in archive:
    print(entry.name)
```

Read content of `file.txt` contained within `file.a`.

```python
with open('file.a') as f:
  archive = Archive(f)
  print(archive.open('file.txt').read())
```

## Author
Samuel Carlsson
