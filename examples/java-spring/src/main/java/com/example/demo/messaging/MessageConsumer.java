package com.example.demo.messaging;

import com.example.demo.domain.Order;
import com.example.demo.repositories.OrderRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.stream.annotation.StreamListener;
import org.springframework.stereotype.Component;

@Component
public class MessageConsumer {
    private static final Logger LOG = LoggerFactory.getLogger(MessageConsumer.class);
    private final OrderRepository orderRepository;

    public MessageConsumer(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @StreamListener(MessageProcessor.ORDER_PLACED)
    public void handleMessage(Order order) {
        LOG.info("Order placed message received with payload: {}", order);
        orderRepository.save(order);
    }
}
