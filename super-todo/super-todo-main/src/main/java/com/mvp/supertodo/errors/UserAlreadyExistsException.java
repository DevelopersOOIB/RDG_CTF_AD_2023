package com.mvp.supertodo.errors;

public class UserAlreadyExistsException extends RuntimeException {

    public UserAlreadyExistsException(String errorMessage) {
        super("User: " + errorMessage + " already exists!");
    }
}
