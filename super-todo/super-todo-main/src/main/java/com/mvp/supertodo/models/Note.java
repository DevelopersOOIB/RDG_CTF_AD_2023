package com.mvp.supertodo.models;

import com.mvp.supertodo.entits.User;
import lombok.*;

import java.time.LocalDateTime;

@Setter
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Note {
    private Long id;
    private String title;
    private String link;
    private String textBody;
    private LocalDateTime timestamp;
    private LocalDateTime completedAt;
    private User user;
    private Boolean isCompleted;
}
