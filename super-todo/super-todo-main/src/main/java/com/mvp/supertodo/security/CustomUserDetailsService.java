package com.mvp.supertodo.security;

import com.mvp.supertodo.enums.*;
import com.mvp.supertodo.errors.UserNotFoundException;
import com.mvp.supertodo.repositories.*;
import lombok.*;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.*;

@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {
    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) {
        var userFromDb = userRepository.findByUsername(username).orElseThrow(UserNotFoundException::new);

        return User.builder()
            .username(userFromDb.getUsername())
            .password(userFromDb.getPassword())
            .authorities(userFromDb.getIsAdmin() ? RoleEnum.ADMIN : RoleEnum.USER)
            .build();
    }
}
