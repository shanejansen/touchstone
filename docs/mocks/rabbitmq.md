Rabbit MQ
======
Used to mock a Rabbit MQ dependency.


## Specs
 * Name: rabbitmq
 * Dev Port: 5672
 * Username: guest
 * Password: guest
 
 
## Configuration
 * `autoCreate` - Default: True. If set to False, queues and exchanges will not be created by Touchstone and should be created by the service instead.


## Defaults Example
```yaml
---
exchanges:
  - name: default-direct.exchange
    type: direct
    queues:
      - name: default-direct1.queue
        routingKey: foo
      - name: default-direct2.queue
  - name: default-fanout.exchange
    type: fanout
    queues:
      - name: default-fanout1.queue
      - name: default-fanout2.queue
  - name: default-topic.exchange
    type: topic
    queues:
      - name: default-topic1.queue
        routingKey: foo
      - name: default-topic2.queue
        routingKey: bar
```


## Usage Example
```python
# Publish a message to an exchange
self.mocks.rabbitmq.setup.publish('default-direct.exchange', 'some payload', routing_key='foo')

# Verify that a certain number of messages were published to an exchange and routing key
result: bool = self.mocks.rabbitmq.verify.messages_published('default-direct.exchange', num_expected=3, routing_key='foo')

# Verify that a payload was published to an exchange and routing key
result: bool = self.mocks.rabbitmq.verify.payload_published('default-topic.exchange', 'some payload', routing_key='foo')
```
