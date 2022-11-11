Mongo DB
======
Used to start a Mongo DB dependency.


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
self.deps.mongodb.setup().insert_document('my_db', 'my_collection', {'foo': 'bar'})

# Verify that a document exists in a collection
result: bool = self.deps.mongodb.verify().document_exists('my_db', 'my_collection', {'foo': 'bar'})
```
