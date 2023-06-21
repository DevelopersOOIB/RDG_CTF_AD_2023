package com.mvp.supertodo.mappers;

import com.mvp.supertodo.dto.*;
import com.mvp.supertodo.models.*;
import org.mapstruct.*;

@MapperConfig(unmappedSourcePolicy = ReportingPolicy.IGNORE, unmappedTargetPolicy = ReportingPolicy.IGNORE)
@Mapper(componentModel = "spring")
public interface MapDtoToModelInt {

    User mapRegisterUserDtoToUserModel(RegisterUser user);

    @Mapping(source = "link", target = "link", qualifiedByName = "formatLink")
    Note mapNoteCreateToNoteEntity(NoteCreate noteCreate);

    @Named("formatLink")
    default String mapFormatLink(String link) {
        if (link.startsWith("http")) {
            return link;
        } else {
            return String.format("http://%s", link);
        }
    }
}
