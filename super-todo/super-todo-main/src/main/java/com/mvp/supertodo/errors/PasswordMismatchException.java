package com.mvp.supertodo.errors;

public class PasswordMismatchException extends RuntimeException {

    public PasswordMismatchException() {
        super("Password mismatch with the old one");
    }

    public PasswordMismatchException(String message) {
        super(message);
    }
}
