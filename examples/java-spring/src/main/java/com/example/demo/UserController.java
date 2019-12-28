package com.example.demo;

import com.example.demo.domain.User;
import com.example.demo.messaging.MessageProducer;
import org.springframework.web.bind.annotation.*;

@RestController
public class UserController {
    private final MessageProducer messageProducer;

    public UserController(MessageProducer messageProducer) {
        this.messageProducer = messageProducer;
    }

    @GetMapping("/user/{id}")
    public User getUser(@PathVariable int id) {
        // TODO
        return null;
    }

    @PostMapping("/user")
    public User postUser(@RequestBody User user) {
        // TODO
        return null;
    }

    @PutMapping("/user")
    public User putUser(@RequestBody User user) {
        // TODO
        return null;
    }

    @DeleteMapping("/user/{id}")
    public void deleteUser(@PathVariable int id) {
        // TODO
        String payload = "UserId: " + id;
        messageProducer.publishUserDeletedMessage(payload);
    }
}
