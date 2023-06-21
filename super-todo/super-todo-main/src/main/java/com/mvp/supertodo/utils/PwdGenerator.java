package com.mvp.supertodo.utils;

import org.springframework.security.crypto.bcrypt.*;
import org.springframework.security.crypto.password.*;

public class PwdGenerator {

    static PasswordEncoder encoder = new BCryptPasswordEncoder();

    public static void main(String[] args) {
        System.out.println("admin pwd: " + encoder.encode("admin"));
        System.out.println("user pwd: " + encoder.encode("user"));
    }
}
