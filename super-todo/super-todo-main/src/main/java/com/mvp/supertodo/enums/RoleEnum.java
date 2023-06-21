package com.mvp.supertodo.enums;

import lombok.*;
import org.springframework.security.core.*;

@RequiredArgsConstructor
public enum RoleEnum implements GrantedAuthority {
    ADMIN("ROLE_ADMIN"),
    USER("ROLE_USER");

    private final String value;

    @Override
    public String getAuthority() {
        return value;
    }

}
