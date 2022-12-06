HTTP
======
Used to start a HTTP dependency.


## Specs
 * Name: http
 * Dev Port: 9090
 
 
## Configuration
N/A


## Defaults Example
```yaml
---
requests:
  - request:
      method: GET
      url: "/api/v1/foo"
    response:
      status: 200
      headers:
        Content-Type: text/plain
      body: Hello HTTP!
  - request:
      method: GET
      url: "/api/v1/bar"
    response:
      status: 200
      headers:
        Content-Type: application/json
      jsonBody:
        {
          "customJson": [
            "Hello",
            "HTTP"
          ],
          "foo": "bar"
        }
```


## Usage Example
```python
# Return JSON when a GET request is made to an endpoint
self.deps.http.setup().get('/some-endpoint', {'foo': 'bar'})

# Verify that an endpoint was called
result: bool = self.deps.http.verify().get_called('/some-endpoint')
```
