package com.mvp.supertodo.entits;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@RequiredArgsConstructor
@ToString
@Entity
public class Note {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;
    private String link;
    private String textBody;
    private LocalDateTime timestamp;
    private LocalDateTime completedAt;
    @ToString.Exclude
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "custom_user_id")
    private User user;
    private Boolean isCompleted;
}
