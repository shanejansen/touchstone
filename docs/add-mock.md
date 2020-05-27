Contribute a New Mock
======
 1. Create a new [Runnable](../touchstone/lib/mocks/runnables) or [Networked Runnable](../touchstone/lib/mocks/networked_runnables)
 1. Add a new property to the [Mocks](../touchstone/lib/mocks/mocks.py) class, so your new mock is accessible in user test cases
 1. Build a concrete instance of your new mock in the [Mock Factory](../touchstone/lib/mocks/mock_factory.py) with its required dependencies
 1. Write [unit](../tests) and [Touchstone tests](../touchstone-tests) for your new mock
