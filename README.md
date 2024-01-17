[![Build Status](https://travis-ci.com/vidstige/ar.svg?branch=master)](https://travis-ci.com/vidstige/ar)

![python-3.8](https://img.shields.io/badge/python-3.8-success)
![python-3.7](https://img.shields.io/badge/python-3.7-success)
![python-3.6](https://img.shields.io/badge/python-3.6-success)
![python-3.5](https://img.shields.io/badge/python-3.5-success)

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
    with open(entry.name) as output:
      content = entry.get_stream().read()
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
