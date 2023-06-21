package com.mvp.supertodo.controllers;

import java.util.*;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.errors.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.ui.*;
import org.springframework.validation.*;
import org.springframework.web.bind.annotation.*;

@Slf4j
@ControllerAdvice
public class CustomExceptionHandler {

    @ExceptionHandler({ UserAlreadyExistsException.class })
    @ResponseStatus(HttpStatus.OK)
    public String handleUserAlreadyExistsException(
        UserAlreadyExistsException exception,
        Model model
    ) {
        RegisterUser registerUser = new RegisterUser();
        FieldError error = new FieldError("registerUser", "username", exception.getMessage());
        BindingResult bindingResult = makeBindingResult(registerUser, "registerUser", Set.of(error));

        model.addAttribute("org.springframework.validation.BindingResult.registerUser", bindingResult);
        model.addAttribute("registerUser", registerUser);
        model.addAttribute("registerError", true);

        return "login";
    }

    @ExceptionHandler({ PasswordMismatchException.class })
    @ResponseStatus(HttpStatus.OK)
    public String handlePasswordMismatchException(
        PasswordMismatchException exception,
        Model model
    ) {
        PasswordUpdate passwordUpdate = new PasswordUpdate();
        FieldError error = new FieldError("passwordUpdate", "oldPassword", exception.getMessage());
        BindingResult bindingResult = makeBindingResult(passwordUpdate, "passwordUpdate", Set.of(error));

        model.addAttribute("org.springframework.validation.BindingResult.passwordUpdate", bindingResult);
        model.addAttribute("passwordUpdate", passwordUpdate);

        return "settings";
    }


    @ExceptionHandler({ Exception.class })
    @ResponseStatus(HttpStatus.I_AM_A_TEAPOT)
    public String handler(Exception exception) {
        log.error(exception.getMessage(), exception);
        return "error";
    }

    private BindingResult makeBindingResult(
        Object object,
        String objectName,
        Set<ObjectError> errors
    ) {
        BindingResult bindingResult = new BeanPropertyBindingResult(object, objectName);
        errors.forEach(bindingResult::addError);
        return bindingResult;
    }
}
