package com.example.demo;

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
