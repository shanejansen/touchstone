Contribute a New Mock
======
 1. Create your mock
 1. Add a new property to the [Mocks](../touchstone/lib/nodes/mocks/mocks.py) class, so your new mock is accessible in user test cases
 1. Build a concrete instance of your new mock in the [Mock Factory](../touchstone/lib/nodes/mocks/mock_factory.py) with its required dependencies
 1. Write [unit](../tests) and [Touchstone tests](../touchstone-tests) for your new mock
