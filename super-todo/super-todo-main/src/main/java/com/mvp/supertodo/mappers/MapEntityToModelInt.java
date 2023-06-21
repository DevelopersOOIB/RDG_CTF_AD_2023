package com.mvp.supertodo.mappers;

import com.mvp.supertodo.models.Note;
import com.mvp.supertodo.models.User;
import org.mapstruct.Mapper;
import org.mapstruct.MapperConfig;
import org.mapstruct.ReportingPolicy;

import java.util.List;

@MapperConfig(unmappedSourcePolicy = ReportingPolicy.IGNORE, unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Mapper(componentModel = "spring")
public interface MapEntityToModelInt {

    User mapUserEntityToUserModel(com.mvp.supertodo.entits.User user);
    Note mapNoteEntityToNoteModel(com.mvp.supertodo.entits.Note note);

    List<Note> mapNoteEntityListToNoteModelList(List<com.mvp.supertodo.entits.Note> noteList);
}
