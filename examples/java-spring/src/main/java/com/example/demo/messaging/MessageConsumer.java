package com.example.demo.messaging;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.stream.annotation.StreamListener;
import org.springframework.stereotype.Component;

@Component
public class MessageConsumer {
    private static final Logger LOG = LoggerFactory.getLogger(MessageConsumer.class);

    @StreamListener(MessageProcessor.ORDER_PLACED)
    public void handleMessage(String payload) {
        LOG.info("Order placed message received with payload: {}", payload);
        // TODO - Write order to Mongo
    }
}
