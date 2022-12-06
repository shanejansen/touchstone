Contribute a New Dependency
======
 1. Create your dependency
 1. Add a new property to the [Dependencies](../touchstone/lib/nodes/deps/deps.py) class, so your new dependency is accessible in user test cases
 1. Build a concrete instance of your new dependency in the [Dependency Factory](../touchstone/lib/nodes/deps/dep_factory.py) with its required dependencies
 1. Write [unit](../tests) and [Touchstone tests](../touchstone-tests) for your new dependency
