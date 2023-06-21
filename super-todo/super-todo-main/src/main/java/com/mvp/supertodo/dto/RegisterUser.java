package com.mvp.supertodo.dto;

import jakarta.validation.constraints.*;
import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RegisterUser {
    @NotBlank(message = "username must not be empty!")
    @Size(min = 4, max = 200, message = "username length must be from 4 to 200")
    private String username;

    @NotBlank(message = "Password must not be empty")
    @Size(min = 4, max = 20, message = "Size must be from 5 to 20 length")
    private String password;

    @NotBlank
    private String repeatPassword;
}
