package com.mvp.supertodo.controllers;

import java.security.*;
import java.util.*;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.dto.request.*;
import com.mvp.supertodo.enums.*;
import com.mvp.supertodo.mappers.*;
import com.mvp.supertodo.models.Note;
import com.mvp.supertodo.services.*;
import lombok.*;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.*;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/notes")
@RequiredArgsConstructor
public class NoteController {

    private final NoteService noteService;
    private final MapDtoToModelInt mapper;
    private final MapModelToDtoInt mapModelToDto;
    private final CheckLinkService checkLinkService;


    @GetMapping
    public String getAll(
        @RequestParam(defaultValue = "ALL") String filter,
        @RequestParam(defaultValue = "TIMESTAMP") String sort,
        Model model,
        Authentication authentication
    ) {
        List<Note> notesModelList = !authentication.getAuthorities().contains(RoleEnum.ADMIN)
            ? noteService.findAllByOwnerNameWithFilterAndSort(authentication.getName(), NoteFilterEnum.valueOf(filter), sort)
            : noteService.findAllWithFilterAndSort(NoteFilterEnum.valueOf(filter), sort);

        List<NoteListDto> notes = mapModelToDto.mapNoteModelListToNoteListDto(notesModelList);
        model.addAttribute("notes", notes);

        return "parts/notes";
    }

    @PostMapping
    public String createNote(@ModelAttribute NoteCreate noteCreate, Principal principal) {
        Note note = mapper.mapNoteCreateToNoteEntity(noteCreate);
        noteService.save(note, principal);
        return "redirect:/todo";
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<StatusResponse> deleteNote(@PathVariable Long id) {
        noteService.deleteById(id);
        return ResponseEntity.ok(new StatusResponse(true));
    }

    @PutMapping("/{id}")
    public String editNote(@PathVariable Long id, @ModelAttribute NoteUpdate noteUpdate) {
        noteService.updateTextBodyByNoteId(id, noteUpdate.getTexBody());
        return "redirect:/todo";
    }

    @CrossOrigin
    @PatchMapping("/{id}/toggle")
    public ResponseEntity<NoteStatus> toggleNote(@PathVariable Long id) {
        var result = noteService.toggleCompletionStatusByNoteId(id);
        return ResponseEntity.ok(mapModelToDto.mapNoteModelToNoteStatusDto(result));
    }

    @CrossOrigin
    @PostMapping(value = "/check-link-availability")
    public ResponseEntity<StatusResponse> checkLinkAvailability(@RequestBody StatusRequest checkLink) {
        String mappedLink = mapper.mapFormatLink(checkLink.getLink());
        var checkLinkResponse = checkLinkService.checkLink(mappedLink);
        return ResponseEntity.ok(checkLinkResponse);
    }



}