package com.mvp.supertodo.controllers;

import java.util.*;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.dto.request.NoteListDto;
import com.mvp.supertodo.enums.*;
import com.mvp.supertodo.mappers.MapModelToDtoInt;
import com.mvp.supertodo.models.Note;
import com.mvp.supertodo.services.*;
import lombok.*;
import org.springframework.security.core.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
public class PagesController {

    private final NoteService noteService;
    private final MapModelToDtoInt mapModelToDto;

    @GetMapping("/todo")
    public String todo(
        @RequestParam(defaultValue = "ALL") String filter,
        @RequestParam(defaultValue = "TIMESTAMP") String sort,
        Authentication authentication,
        Model model
    ) {
        List<Note> notesModelList = !authentication.getAuthorities().contains(RoleEnum.ADMIN)
            ? noteService.findAllByOwnerNameWithFilterAndSort(authentication.getName(), NoteFilterEnum.valueOf(filter), sort)
            : noteService.findAllWithFilterAndSort(NoteFilterEnum.valueOf(filter), sort);

        List<NoteListDto> notes = mapModelToDto.mapNoteModelListToNoteListDto(notesModelList);

        model.addAttribute("notes", notes);
        model.addAttribute("noteCreate", new NoteCreate());

        return "todo";
    }

    @GetMapping("/login")
    private String login(Model model) {
        model.addAttribute("registerUser", new RegisterUser());
        return "login";
    }

    @GetMapping("/settings")
    private String settings(Model model) {
        model.addAttribute("passwordUpdate", new PasswordUpdate());
        return "settings";
    }

}