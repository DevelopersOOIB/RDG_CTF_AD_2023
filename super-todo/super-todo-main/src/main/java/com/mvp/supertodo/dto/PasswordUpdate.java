package com.mvp.supertodo.dto;

import jakarta.validation.constraints.*;
import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PasswordUpdate {

    private String oldPassword;

    @NotBlank(message = "Password must not be empty")
    @Size(min = 4, max = 20, message = "Size must be from 5 to 20 length")
    private String newPassword;
}
