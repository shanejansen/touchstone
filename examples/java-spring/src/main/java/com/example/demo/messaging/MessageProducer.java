package com.example.demo.messaging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.MessageBuilder;
import org.springframework.stereotype.Component;

@Component
public class MessageProducer {
    private static final Logger LOG = LoggerFactory.getLogger(MessageProducer.class);
    private final MessageProcessor messageProcessor;

    public MessageProducer(MessageProcessor messageProcessor) {
        this.messageProcessor = messageProcessor;
    }

    public void publishMessage(String payload) {
        Message<String> message = MessageBuilder.withPayload(payload).build();
        messageProcessor.output().send(message);
    }
}
