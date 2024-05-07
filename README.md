![build](https://github.com/vidstige/ar/actions/workflows/python-package.yml/badge.svg)

![python-3.11](https://img.shields.io/badge/python-3.11-success)
![python-3.10](https://img.shields.io/badge/python-3.10-success)
![python-3.9](https://img.shields.io/badge/python-3.9-success)
![python-3.8](https://img.shields.io/badge/python-3.8-success)
![python-3.7](https://img.shields.io/badge/python-3.7-success)


# ar
Python package for parsing ar archive file. 

## Installation
`pip install ar`

## Usage
List files inside `file.a`
```python
from ar import Archive
with open('file.a', 'rb') as f:
  archive = Archive(f)
  for entry in archive:
    print(entry.name)
```

Read content of `file.txt` contained within `file.a`.

```python
from ar import Archive
with open('file.a', 'rb') as f:
  archive = Archive(f)
  print(archive.open('file.txt').read())
```

Extract all files:
```python
from ar import Archive
with open('file.a', 'rb') as f:
  archive = Archive(f)
  for entry in archive:
    with open(entry.name, 'wb') as output:
      content = archive.open(entry, 'rb').read()
      output.write(content)
```

## Developing
Create a virtual environment using python version of liking

    python3.10 -m venv venv
  
Activate it

    source venv/bin/activate

Install package editable together with relevant optional dependencies

    pip install -e '.[test,dev]'

## Author
Samuel Carlsson
