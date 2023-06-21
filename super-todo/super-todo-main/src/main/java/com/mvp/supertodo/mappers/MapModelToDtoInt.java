package com.mvp.supertodo.mappers;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.dto.request.NoteListDto;
import com.mvp.supertodo.models.Note;
import org.mapstruct.*;

import java.util.List;

@MapperConfig(unmappedSourcePolicy = ReportingPolicy.IGNORE, unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Mapper(componentModel = "spring")
public interface MapModelToDtoInt {

    NoteListDto mapNoteListDto(Note note);

    NoteStatus mapNoteModelToNoteStatusDto(Note note);

    List<NoteListDto> mapNoteModelListToNoteListDto(List<Note> noteList);
}
