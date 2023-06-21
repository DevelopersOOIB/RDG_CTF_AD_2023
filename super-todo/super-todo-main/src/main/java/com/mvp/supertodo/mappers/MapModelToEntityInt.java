package com.mvp.supertodo.mappers;

import com.mvp.supertodo.entits.Note;
import com.mvp.supertodo.entits.User;
import org.mapstruct.*;

@MapperConfig(unmappedSourcePolicy = ReportingPolicy.IGNORE, unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Mapper(componentModel = "spring")
public interface MapModelToEntityInt {

    User mapUserModelToUserEntity(com.mvp.supertodo.models.User user);

    Note mapNoteModelToNoteEntity(com.mvp.supertodo.models.Note note);
}
