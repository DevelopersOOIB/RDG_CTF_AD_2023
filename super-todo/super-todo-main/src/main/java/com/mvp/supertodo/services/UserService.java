package com.mvp.supertodo.services;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.errors.*;
import com.mvp.supertodo.mappers.MapModelToEntityInt;
import com.mvp.supertodo.models.*;
import com.mvp.supertodo.repositories.*;
import jakarta.transaction.Transactional;
import lombok.*;
import org.springframework.security.crypto.password.*;
import org.springframework.stereotype.*;


@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;
    private final PasswordEncoder passwordEncoder;
    private final MapModelToEntityInt mapModelToEntity;

    @Transactional
    public void save(@NonNull User user) {
        if (repository.findByUsername(user.getUsername()).isPresent()) {
            throw new UserAlreadyExistsException(user.getUsername());
        }

        var userEntity = mapModelToEntity.mapUserModelToUserEntity(user);
        userEntity.setPassword(passwordEncoder.encode(user.getPassword()));
        userEntity.setIsAdmin(false);

        repository.save(userEntity);
    }

    @Transactional
    public void changePassword(@NonNull PasswordUpdate passwordUpdate, String username) {
        var userEntity = repository
            .findByUsername(username)
            .orElseThrow(UserNotFoundException::new);

        if(!passwordEncoder.matches(passwordUpdate.getOldPassword(), userEntity.getPassword())) {
            throw new PasswordMismatchException();
        }

        userEntity.setPassword(passwordEncoder.encode(passwordUpdate.getNewPassword()));
        repository.save(userEntity);
    }

}
