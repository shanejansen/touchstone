package com.example.demo.repositories;

import com.example.demo.domain.User;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class UserRepository {
    private final NamedParameterJdbcTemplate jdbcTemplate;

    public UserRepository(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public User get(int id) {
        String sql = "SELECT * FROM users WHERE id = :id";
        Map<String, String> params = new HashMap<>();
        params.put("id", String.valueOf(id));
        return jdbcTemplate.queryForObject(sql, params, (resultSet, i) -> new User(
                resultSet.getInt("id"),
                resultSet.getString("first_name"),
                resultSet.getString("last_name"),
                resultSet.getString("email")
        ));
    }

    public User save(User user) {
        String sql = "INSERT INTO users (first_name, last_name, email) VALUES (:firstName, :lastName, :email)";
        Map<String, String> params = new HashMap<>();
        params.put("firstName", user.getFirstName());
        params.put("lastName", user.getLastName());
        params.put("email", user.getEmail());
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbcTemplate.update(sql, new MapSqlParameterSource(params), keyHolder);
        user.setId(keyHolder.getKey().intValue());
        return user;
    }

    public void update(User user) {
        String sql = "UPDATE users SET first_name = :firstName, last_name = :lastName, email = :email WHERE id = :id";
        Map<String, String> params = new HashMap<>();
        params.put("firstName", user.getFirstName());
        params.put("lastName", user.getLastName());
        params.put("email", user.getEmail());
        params.put("id", String.valueOf(user.getId()));
        jdbcTemplate.update(sql, params);
    }

    public void delete(int id) {
        String sql = "DELETE FROM users WHERE id = :id";
        Map<String, String> params = new HashMap<>();
        params.put("id", String.valueOf(id));
        jdbcTemplate.update(sql, params);
    }
}
