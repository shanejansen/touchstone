package com.example.demo.messaging;

import org.springframework.cloud.stream.annotation.Input;
import org.springframework.cloud.stream.annotation.Output;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.SubscribableChannel;

public interface MessageProcessor {
    String ORDER_PLACED = "order-placed";
    String USER_DELETED = "user-deleted";

    @Input(ORDER_PLACED)
    SubscribableChannel orderPlaced();

    @Output(USER_DELETED)
    MessageChannel userDeleted();
}
