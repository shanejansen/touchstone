Filesystem
======
Used to start a filesystem for verifying file creation and contents.

All filesystem I/O must be handled in the `touchstone/io` directory. This allows service containers to access the directory on your local machine using a bind mount. All files used in validation, whether created via a test, or the service itself, should be written to this directory.  
Note: All paths used in the "setup" and "verify" APIs use the `touchstone/io` directory as a base path.


## Specs
 * Name: filesystem
 
 
## Configuration
N/A


## Defaults Example
A YAML file is not supplied for the filesystem dependency. A directory with name `filesystem` is used instead. All files in this directory are copied to `touchstone/io` before each test.  
[Example](../../examples/python-spark/touchstone/defaults/filesystem)


## Usage Example
```python
# Verify a file exists in a directory
result: bool = self.deps.filesystem.verify().file_exists('foo.csv')

# Verify a file's content matches as expected
result: bool = self.deps.filesystem.verify().file_matches('foo.csv', given)
```

If you are performing filesystem operations in your test code, you must join with `get_io_path` when referring to file paths. This returns the path to the `touchstone/io` folder. For example:
```python
path = os.path.join(self.deps.filesystem.get_io_path(), 'foo.csv')
with open(path, 'rb') as data:
    return bytes(data.read())
```
