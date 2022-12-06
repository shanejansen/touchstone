Redis
======
Used to start a Redis data store dependency.

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
self.deps.redis.setup().set('foo')

# Get a value
self.deps.redis.verify().get('foo')

# Get a JSON value as dict
result: dict = self.deps.redis.verify().get_json('foo')
```
