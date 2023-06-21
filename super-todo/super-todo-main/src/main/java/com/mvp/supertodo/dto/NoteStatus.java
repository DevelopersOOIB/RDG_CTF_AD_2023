package com.mvp.supertodo.dto;

import lombok.*;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteStatus {
    private Long id;
    private Boolean isCompleted;
}
