package com.example.demo.domain;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "orders")
public class Order {
    @Id
    private String id;
    private int userId;
    private String item;
    private int quantity;

    public String getId() {
        return id;
    }

    public int getUserId() {
        return userId;
    }

    public String getItem() {
        return item;
    }

    public int getQuantity() {
        return quantity;
    }

    @Override
    public String toString() {
        return "Order{" +
                "id='" + id + '\'' +
                ", userId=" + userId +
                ", item='" + item + '\'' +
                ", quantity=" + quantity +
                '}';
    }
}
