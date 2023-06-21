package com.mvp.supertodo.repositories;

import java.util.*;

import com.mvp.supertodo.entits.*;
import jakarta.persistence.*;
import lombok.NonNull;
import org.springframework.stereotype.*;


@Repository
public class UserRepository {

    @PersistenceContext
    private EntityManager entityManager;

    public Optional<User> findByUsername(@NonNull String username) {
        User user = null;
        try {
            user = (User) entityManager
                .createNativeQuery(
                    String.format(
                        """
                            SELECT * FROM custom_user
                            WHERE username = '%s'
                        """,
                        username
                    ),
                    User.class
                ).getSingleResult();
            entityManager.close();
        } catch (NoResultException err) {
            return Optional.empty();
        }
        return Optional.ofNullable(user);
    }

    public void save(@NonNull User user) {
        entityManager.persist(user);
        entityManager.close();
    }
}

