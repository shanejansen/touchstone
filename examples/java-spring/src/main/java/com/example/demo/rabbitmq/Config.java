package com.example.demo.rabbitmq;

import org.springframework.cloud.stream.annotation.Input;
import org.springframework.messaging.SubscribableChannel;

public interface Config {
    String INPUT = "input";

    @Input(INPUT)
    SubscribableChannel input();
}
