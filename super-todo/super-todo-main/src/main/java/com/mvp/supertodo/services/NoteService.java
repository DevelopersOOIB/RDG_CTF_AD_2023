package com.mvp.supertodo.services;

import java.security.Principal;
import java.time.LocalDateTime;
import java.util.*;

import com.mvp.supertodo.enums.*;
import com.mvp.supertodo.errors.UserNotFoundException;
import com.mvp.supertodo.mappers.MapEntityToModelInt;
import com.mvp.supertodo.mappers.MapModelToEntityInt;
import com.mvp.supertodo.models.Note;
import com.mvp.supertodo.repositories.*;
import lombok.*;
import org.springframework.stereotype.*;
import org.springframework.web.bind.annotation.*;

@Service
@RequiredArgsConstructor
public class NoteService {

    private final NoteRepository noteRepository;
    private final UserRepository userRepository;
    private final MapModelToEntityInt mapModelToEntity;
    private final MapEntityToModelInt mapEntityToModel;


    public List<Note> findAllWithFilterAndSort(
        @NonNull NoteFilterEnum filter,
        @NonNull String sort
    ) {
        var noteEntityList = switch (filter) {
            case ALL -> noteRepository.findAllWithSort(sort);
            case ACTIVE -> noteRepository.findAllWithFilterAndSort(false, sort);
            case COMPLETED -> noteRepository.findAllWithFilterAndSort(true, sort);
        };

        return mapEntityToModel.mapNoteEntityListToNoteModelList(noteEntityList);
    }

    public List<Note> findAllByOwnerNameWithFilterAndSort(
        @NonNull String name,
        @NonNull NoteFilterEnum filter,
        @NonNull String sort
    ) {
        var noteEntityList = switch (filter) {
            case ALL -> noteRepository.findAllByOwnerUsernameWithSort(name, sort);
            case ACTIVE -> noteRepository.findAllByOwnerUsernameWithFilterAndSort(name, false, sort);
            case COMPLETED -> noteRepository.findAllByOwnerUsernameWithFilterAndSort(name, true, sort);
        };

        return mapEntityToModel.mapNoteEntityListToNoteModelList(noteEntityList);
    }

    public void save(@NonNull Note note, Principal principal) {
        note.setUser(
            userRepository
                .findByUsername(principal.getName())
                .orElseThrow(UserNotFoundException::new)
        );
        note.setTimestamp(LocalDateTime.now());
        note.setIsCompleted(false);
        noteRepository.save(
            mapModelToEntity.mapNoteModelToNoteEntity(note)
        );
    }

    public Note toggleCompletionStatusByNoteId(@NonNull Long id) {
        noteRepository.toggleCompletionStatusByNoteId(id, LocalDateTime.now());
        return mapEntityToModel.mapNoteEntityToNoteModel(noteRepository.findById(id));
    }

    public void updateTextBodyByNoteId(@NonNull Long id, @NonNull String textBody) {
        noteRepository.updateTextBodyByNoteId(id, textBody);
    }

    public void deleteById(@NonNull Long id) {
        noteRepository.deleteNoteById(id);
    }
}
