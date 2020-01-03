package com.example.demo.gateways;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;

@Service
public class EmailGateway {
    private final String serviceUrl;
    private final RestTemplate restTemplate;


    public EmailGateway(@Value("${app.email-service}") String serviceUrl, RestTemplate restTemplate) {
        this.serviceUrl = serviceUrl;
        this.restTemplate = restTemplate;
    }

    public String emailForName(String firstName, String lastName) {
        URI uri = UriComponentsBuilder.fromUriString(serviceUrl)
                .pathSegment(firstName.toLowerCase() + "-" + lastName.toLowerCase(), "email")
                .build()
                .toUri();
        return restTemplate.getForEntity(uri.toString(), String.class).getBody();
    }
}
