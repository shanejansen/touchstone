Mongo DB
======
Used to mock a Mongo DB dependency.


## Specs
 * Name: mongodb
 * Dev Port: 27017
 
 
## Configuration
N/A


## Defaults Example
```yaml
---
databases:
  - name: myapp
    collections:
      - name: users
        documents:
          - {"firstName": "John", "lastName": "Smith"}
          - {"firstName": "Jane", "lastName": "Brown"}
```


## Usage Example
```python
# Insert a document into a collection
self.mocks.mongodb.setup.insert_document('my_db', 'my_collection', {'foo': 'bar'})

# Verify that a document was inserted into a collection
result: bool = self.mocks.mongodb.verify.document_exists('my_db', 'my_collection', {'foo': 'bar'})
```
