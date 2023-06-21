package com.mvp.supertodo.controllers;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.mappers.MapDtoToModelInt;
import com.mvp.supertodo.models.*;
import com.mvp.supertodo.services.*;
import jakarta.validation.*;
import lombok.*;
import org.springframework.security.core.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.*;
import org.springframework.validation.*;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.mvc.support.*;


@Controller
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService service;
    private final MapDtoToModelInt mapper;

    @PostMapping("/signup")
    public String signup(
        @Valid @ModelAttribute RegisterUser registerUser,
        BindingResult bindingResult,
        RedirectAttributes redirectAttributes,
        Model model
    ) {
        if (bindingResult.hasFieldErrors()) {
            model.addAttribute("registerError", true);
            return "login";
        }

        User user = mapper.mapRegisterUserDtoToUserModel(registerUser);
        service.save(user);

        redirectAttributes.addFlashAttribute("registered", true);
        return  "redirect:/login";
    }

    @PostMapping("/pwd-change")
    public String changePassword(
        @Valid @ModelAttribute PasswordUpdate passwordUpdate,
        BindingResult bindingResult,
        Authentication authentication,
        RedirectAttributes redirectAttributes
    ) {
        if(bindingResult.hasErrors()) {
            return "settings";
        }

        service.changePassword(passwordUpdate, authentication.getName());
        redirectAttributes.addFlashAttribute("pwdChanged", true);

        return "redirect:/settings";
    }

}
