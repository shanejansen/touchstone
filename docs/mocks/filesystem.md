Filesystem
======
Used to mock a filesystem for verifying file creation and contents.

Note: All paths used in the "setup" and "verify" APIs use the "defaults" directory as a base path.


## Specs
 * Name: filesystem
 
 
## Configuration
N/A


## Defaults Example
**WARNING:** Each path listed under `directories` is deleted after each test! This ensures consistency between tests as files are re-copied.

```yaml
---
directories:
  - path: ./filesystem/some-dir
    files:
      - ./filesystem/foo.csv
      - ./filesystem/bar.png
  - path: ./filesystem/some-dir/sub-dir
    files:
      - ./filesystem/foo.csv
```


## Usage Example
```python
# Verify a file exists in a directory
result: bool = self.mocks.filesystem.verify().file_exists('./filesystem/some-dir/foo.csv')

# Verify a file's content matches as expected
result: bool = self.mocks.filesystem.verify().file_matches('./filesystem/some-dir/foo.csv', given)
```

If you are performing filesystem operations in your test code, you must join with `get_base_path` when referring to file paths. This returns the path to the "defaults" folder. For example:
```python
path = os.path.join(self.mocks.filesystem.get_base_path(), './filesystem/foo.csv')
with open(path, 'rb') as data:
    return bytes(data.read())
```
