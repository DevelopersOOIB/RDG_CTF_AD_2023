package com.mvp.supertodo.dto.request;

import lombok.*;

import java.time.LocalDateTime;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NoteListDto {
    private Long id;
    private String title;
    private String link;
    private String textBody;
    private LocalDateTime timestamp;
    private LocalDateTime completedAt;
    private Boolean isCompleted;
    private String createdBy;
}
