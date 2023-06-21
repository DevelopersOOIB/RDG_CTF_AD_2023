package com.mvp.supertodo.dto;

import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteCreate {
    private String title;
    private String link;
    private String textBody;
}