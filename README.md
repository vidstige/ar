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
