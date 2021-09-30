Redis
======
Used to mock a Redis data store dependency.

## Specs

* Name: redis
* Dev Port: 6379
* Password:

## Configuration

N/A

## Defaults Example

```yaml
---
objects:
  foo: bar
  baz: buzz
```

## Usage Example

```python
# Set a value
self.mocks.redis.setup().set('foo')

# Get a value
self.mocks.redis.verify().get('foo')

# Get a JSON value as dict
result: dict = self.mocks.redis.verify().get_json('foo')
```
