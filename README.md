Touchstone
======
![Unit Tests](https://github.com/shane-jansen/touchstone/workflows/Unit%20Tests/badge.svg?branch=develop)
![Touchstone Tests](https://github.com/shane-jansen/touchstone/workflows/Touchstone%20Tests/badge.svg?branch=develop)

Touchstone is a testing framework for your services that focuses on [component](https://martinfowler.com/articles/microservice-testing/#testing-component-out-of-process-diagram), [end-to-end](https://martinfowler.com/articles/microservice-testing/#testing-end-to-end-introduction), and [exploratory](https://martinfowler.com/bliki/ExploratoryTesting.html) testing.  


## Introduction
![Testing Pyramid](./docs/images/testing-pyramid.png)  
[Image Credit](https://martinfowler.com/articles/microservice-testing/#conclusion-test-pyramid)

Touchstone aims to simplify the top three pieces of the testing pyramid by providing mock implementations of common service dependencies and exposing them via an easy to use testing framework. Whether your app is written in Java, Python, Go, C#, [Fortran](https://www.fortran.io/), or any other language, Touchstone handles its dependencies while you focus on writing tests. Not a single line of component or end-to-end testing code needs to change should you decide to refactor or rewrite your service.


## Use Case
Let's say we are building a microservice that is responsible for managing users. The service exposes a REST API and the requirements for each endpoint are as follows:
 * `GET /user/{id}` - A user is retrieved from a relational database and returned.
 * `POST /user` - A new user is submitted with a first name and last name. An HTTP call is made to an _Email Service_ where an email is returned for that user. The new user is then saved in a relational database and returned.
 * `PUT /user` - A user's id, first name, last name, and email are submitted and then updated in a relational database.
 * `DELETE /user/{id}` - A user is deleted from a relational database. A message is also published to a broker on the exchange: 'user.exchange' with a routing key of: 'user-deleted' and a payload containing the user's id.
 * The service is also listening for messages published to the exchange: 'order-placed.exchange'. When a message is received, the order payload is saved to a NoSQL database.

With Touchstone, it is possible to write component and end-to-end tests for all of the above requirements independent of the language/framework used. For example, we can write a component test for the `DELETE /user/{id}` endpoint that will ensure the user record is removed from the database and a message is published to the correct exchange with the correct payload. When ran, Touchstone will monitor mock instances of the service's dependencies to ensure the requirements are met. Touchstone also makes it easy to perform exploratory testing locally during development by starting dependencies and populating them with data in a single command.

An example of the above requirements is implemented in a Java/Spring service in this repo. Touchstone tests have been written to test the [user endpoint requirements](./examples/java-spring/touchstone/tests/test_user.py) and [order messaging requirements](./examples/java-spring/touchstone/tests/test_order.py).


## Installation
`pip install touchstone-testing`

Requirements:
 * Python 3.6+
 * Docker


## Usage
After installation, Touchstone will be available via `touchstone` in your terminal.  
Touchstone has three basic commands:
 * `touchstone init` - Initialize Touchstone in the current directory. Used for new projects.
 * `touchstone run` - Run all Touchstone tests and exit. This is typically how you would run your Touchstone tests on a build server. Ports will be auto-discovered in this mode to avoid collisions in case multiple runs occur on the same host. See [mocks docs](#mocks) for more information on how to hook into auto-discovered ports.
 * `touchstone develop` - Start a development session of Touchstone. You would typically use this to develop/debug a service locally. This will keep service dependencies running while you make changes to your Touchstone tests or the services themselves. This will also provide a web interface to each mock dependency for additional debugging. Mocked dependencies can be altered or reset on the fly to make exploratory testing easier.
 
After running `touchstone init`, a new directory will be created with the following contents:

### `/touchstone.yml`
[Example](./examples/java-spring/touchstone/touchstone.yml)  
Your services and their monitored dependencies are defined here. Default values should be enough in most cases.
 * `host:` - Default: localhost. The host where your services are running.
 * `services:` - Each service included in your Touchstone tests is defined here.
   * `name:` - Default: unnamed-service. The name of the service.
   * `tests:` - Default: ./tests. The path to Touchstone tests for this service.
   * `host:` - Default: parent host. Fine-grained host control per service.
   * `port:` - Default: 8080. The port used for this service.
   * `dockerfile:` - Default: N/A. Used to containerize the service during `touchstone run`. If you are only running Touchstone locally, this can be omitted.
   * `availability_endpoint:` - Default: N/A. Used to determine when the service is healthy so tests can be executed. A HTTP status `2xx` must be returned from the endpoint to be considered healthy.
   * `num_retries:` - Default: 20. The number of times Touchstone will try to successfully call the `availability_endpoint`.
   * `seconds_between_retries:` - Default: 5. The number of seconds between each retry.
 * `mocks:` - Each mock dependency your service(s) are being tested against.
   * This is how Touchstone determines which mocked dependencies should be started.
   * View each [mock's docs](#mocks) for values and additional configuration.

### `/defaults`
[Example](./examples/java-spring/touchstone/defaults/mysql.yml)  
This directory contains YAML files where default values for mocked dependencies are defined. Defaults make it easy to test your service(s) locally by setting up your mock dependencies with sensible defaults. The name of each YAML file should match the name of a mock. For instance, with the MySQL mock, a `mysql.yml` file would contain default databases and tables to be created as well as statements to insert initial data. View each [mock's docs](#mocks) for allowable values.


### `/tests`
[Example](./examples/java-spring/touchstone/tests)  
This directory is the default location for your Touchstone tests. This can optionally be configured for each service in `touchstone.yml`.  
Touchstone follows a _given_, _when_, _then_ testing pattern. Each test is declared in a Python file prefixed with `test_` containing classes that extend `TouchstoneTest`. By extending this class, you can access Touchstone mocked dependencies to setup and then verify your requirements. For example, we can insert a document into a Mongo DB collection and then verify it exists using the following APIs:
```python
self.mocks.mongodb.setup().insert_document('my_db', 'my_collection', {'foo': 'bar'})
result: bool = self.mocks.mongodb.verify().document_exists('my_db', 'my_collection', {'foo': 'bar'})
```
Important APIs:
 * `self.mocks` - Hook into Touchstone managed mock dependencies.
 * `self.service_url` - The service under test's URL. Useful for calling RESTful endpoints on the service under test.
 * `touchstone.lib.mocks.validation` - Contains methods for validating test results. `validation.ANY` can be used to accept any value which is useful in some circumstances.

## Mocks
 * [HTTP](./docs/mocks/http.md)
 * [Mongo DB](./docs/mocks/mongodb.md)
 * [MySQL](./docs/mocks/mysql.md)
 * [Rabbit MQ](./docs/mocks/rabbitmq.md)
 * [S3](./docs/mocks/s3.md)
 * [Filesystem](./docs/mocks/filesystem.md)
 * [Add one!](./docs/add-mock.md)
 
If a specific mock is not supported, consider building your service independent of the implementation layer. For example, if you have a dependency on PostgreSQL, use the MySQL mock as your database implementation during testing.
 
When running via `touchstone develop`, dev ports for each mock are used. When running touchstone via `touchstone run`, ports are automatically discovered and available to your service containers via the following environment variables:
 * `TS_{MOCK_NAME}_HOST` - Host where the mock is running.
 * `TS_{MOCK_NAME}_PORT` - Port where the mock is running.
 * `TS_{MOCK_NAME}_URL` - Complete URL where the mock is running.
 * `TS_{MOCK_NAME}_USERNAME` - Username for authenticating with the mock.
 * `TS_{MOCK_NAME}_PASSWORD` - Password for authenticating with the mock.
