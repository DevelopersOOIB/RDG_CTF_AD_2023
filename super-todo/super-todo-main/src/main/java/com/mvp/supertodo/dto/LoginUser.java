package com.mvp.supertodo.dto;

import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginUser {
    private String username;
    private String password;
}
