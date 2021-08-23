package com.example.demo.controllers;

import com.example.demo.domain.User;
import com.example.demo.gateways.EmailGateway;
import com.example.demo.messaging.MessageProducer;
import com.example.demo.repositories.UserRepository;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
    private final UserRepository userRepository;
    private final EmailGateway emailGateway;
    private final MessageProducer messageProducer;

    public UserController(UserRepository userRepository, EmailGateway emailGateway, MessageProducer messageProducer) {
        this.userRepository = userRepository;
        this.emailGateway = emailGateway;
        this.messageProducer = messageProducer;
    }

    @GetMapping("/user/{id}")
    public User getUser(@PathVariable int id) {
        return userRepository.get(id);
    }

    @PostMapping("/user")
    public User postUser(@RequestBody User user) {
        String email = emailGateway.emailForName(user.getFirstName(), user.getLastName());
        user.setEmail(email);
        return userRepository.save(user);
    }

    @PutMapping("/user")
    public void putUser(@RequestBody User user) {
        userRepository.update(user);
    }

    @DeleteMapping("/user/{id}")
    public void deleteUser(@PathVariable int id) {
        userRepository.delete(id);
        messageProducer.publishUserDeletedMessage(String.valueOf(id));
    }
}
