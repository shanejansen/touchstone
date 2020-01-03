package com.example.demo;

import com.example.demo.domain.User;
import com.example.demo.gateways.EmailGateway;
import com.example.demo.messaging.MessageProducer;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
    private final EmailGateway emailGateway;
    private final MessageProducer messageProducer;

    public UserController(EmailGateway emailGateway, MessageProducer messageProducer) {
        this.emailGateway = emailGateway;
        this.messageProducer = messageProducer;
    }

    @GetMapping("/user/{id}")
    public User getUser(@PathVariable int id) {
        // TODO: Get user from relational db
        return null;
    }

    @PostMapping("/user")
    public User postUser(@RequestBody User user) {
        // TODO: Save user to relational db
        String email = emailGateway.emailForName(user.getFirstName(), user.getLastName());
        user.setEmail(email);
        return user;
    }

    @PutMapping("/user")
    public User putUser(@RequestBody User user) {
        // TODO: Update user in relational db
        return null;
    }

    @DeleteMapping("/user/{id}")
    public void deleteUser(@PathVariable int id) {
        // TODO: Remove user from relational db
        messageProducer.publishUserDeletedMessage(String.valueOf(id));
    }
}
