Touchstone
======
Touchstone is a testing framework for your services that focuses on [end-to-end](https://www.martinfowler.com/bliki/BroadStackTest.html) and [exploratory](https://martinfowler.com/bliki/ExploratoryTesting.html) testing.  
**Touchstone is currently in alpha and APIs may change without warning.**


## Introduction
![Testing Pyramid](./docs/images/testing-pyramid.png)  
[Image Credit](https://martinfowler.com/articles/microservice-testing/#conclusion-test-pyramid)

Touchstone aims to simplify these two pieces of the testing pyramid by providing real implementations of common service dependencies and exposing them via an easy to use testing framework. Whether your app is written in Java, Python, Go, C#, [Fortran](https://www.fortran.io/), or any other language, Touchstone handles its dependencies while you focus on writing tests. Not a single line of end-to-end testing code needs to change should you decide to refactor or rewrite your service.


## Example
Let's say we are building a microservice that is responsible for managing users. The service exposes a REST API and the requirements for each endpoint are as follows:
 * `GET /user/{id}` - A user is retrieved from a relational database and returned.
 * `POST /user` - A new user is submitted with a first name and last name. An HTTP call is made to an _Email Service_ where an email is returned for that user. The new user is then saved in a relational database and returned.
 * `PUT /user` - A user's id, first name, last name, and email are submitted and then updated in a relational database.
 * `DELETE /user/{id}` - A user is deleted from a relational database. A message is also published to a broker on the exchange: 'user.exchange' with a routing key of: 'user-deleted' and a payload containing the user's id.
 * The service is also listening for messages published to the exchange: 'order-placed.exchange'. When a message is received, the order payload is saved to a NoSQL database.

With Touchstone, it is possible to write end-to-end tests for all the above requirements independent of the language/framework used. When ran, Touchstone will monitor real instances of the service's dependencies to ensure its requirements are met. Touchstone also makes it easy to perform exploratory testing locally during development by starting dependencies and populating them with mock data via a single command.

An example of the above requirements are implemented in a Java/Spring service in this repo. Touchstone tests have been written to test the [user endpoint requirements](./examples/java-spring/touchstone/tests/user.py) and [order messaging requirements](./examples/java-spring/touchstone/tests/order.py).


## Installation
`pip install touchstone-testing`

Requirements:
 * Python 3.6+
 * Docker


## Usage
After installation, Touchstone will be available via `touchstone` in your terminal.  
Touchstone has three base commands:
 * `touchstone init` - Initialize Touchstone in the current directory. Used for new projects.
 * `touchstone run` - Run all Touchstone tests and exit. This is typically how you'd run your end-to-end tests on a build server. Service and dependency ports will be auto-discovered in this mode to avoid collisions in case multiple runs occur on the same host. See [Suppored Dependencies](#supported-dependencies) for more information on how to hook into auto-discovered dependencies.
 * `touchstone develop` - Start a development session of Touchstone. You'd typically use this to develop/debug a service locally. This will keep service dependencies running while you make changes to your end-to-end tests or the services themselves. This will also provide a web interface to each dependency for additional debugging. 
 
After running `touchstone init`, a new directory will be created with the following contents:

### `touchstone.yml`
Your services and their monitored dependencies are defined here. Default values should be enough in most cases. [Example](./examples/java-spring/touchstone/touchstone.yml)
 * `host:` - Default: localhost. The host where your services are running.
 * `services:` - Each service included in your end-to-end tests are defined here.
   * `name:` - Default: unnamed-service. The name of the service.
   * `tests:` - Default: ./tests. The path to Touchstone tests for this service.
   * `host:` - Default: parent host. Fine grained host control per service.
   * `port:` - Default: 8080. The port used for this service.
   * `dockerfile:` - Default: N/A. Used to containerize the service during `touchstone run`. If you are only running Touchstone locally, this can be omitted.
   * `availability_endpoint:` - Default: N/A. Used to determine when the service is healthy so tests can be executed. A `200` must be returned from the endpoint to be considered healthy.
   * `num_retries:` - Default: 20. The number of times Touchstone will try to successfully call the `availability_endpoint`.
   * `seconds_between_retries:` - Default: 5. The number of seconds between each retry.
 * `mocks:`

 
### Writing Tests
Touchstone end-to-end tests are written in Python. 


## Supported Dependencies
 * HTTP
 * Mongo DB
 * MySQL
 * Rabbit MQ
 
Don't see a dependency you want to include in your testing? [Add it!](./docs/under-construction.md)
