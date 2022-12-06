MySQL
======
Used to start a MySQL dependency.


## Specs
 * Name: mysql
 * Dev Port: 3306
 * Username: root
 * Password: root
 
 
## Configuration
 * `camel_to_snake` - Default: True. When supplying a dict to this dependency's API, this value determines if the dict keys should be converted to snake case to match MySQL's convention.
 * `snapshot_databases` - Default: False. When set to True, a snapshot of the database(s) specified in the defaults file is taken when the services become healthy. This snapshot is then used during each reset of the dependency. This can be useful if your app uses a database migration tool (e.g. Flyway) where some initial data is inserted by the apps themselves.


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
self.deps.mysql.setup().insert_row('my_db', 'my_table', {'foo': 'bar'})

# Verify that a row exists in a table
result: bool = self.deps.mysql.verify().row_exists('my_db', 'my_table', {'foo': 'bar'})
```
