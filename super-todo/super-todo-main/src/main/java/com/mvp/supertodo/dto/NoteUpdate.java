package com.mvp.supertodo.dto;

import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteUpdate {
    private String title;
    private String texBody;
}