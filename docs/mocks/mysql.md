My SQL
======
Used to mock a My SQL dependency.


## Specs
 * Name: mysql
 * Dev Port: 3306
 * Username: root
 * Password: root
 
 
## Configuration
 * `convertCamelToSnakeCase` - Default: True. When supplying a dict to this mock's API, this value determines if the dict keys should be converted to snake case to match My SQL's convention.


## Defaults Example
```yaml
---
databases:
  - name: myapp
    statements:
      - "CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255))"
      - "INSERT INTO users VALUES ('John', 'Smith')"
      - "INSERT INTO users VALUES ('Jane', 'Brown')"
```


## Usage Example
```python
# Insert a row into a table
self.mocks.mysql.setup().insert_row('my_db', 'my_table', {'foo': 'bar'})

# Verify that a row exists in a table
result: bool = self.mocks.mysql.verify().row_exists('my_db', 'my_table', {'foo': 'bar'})
```
