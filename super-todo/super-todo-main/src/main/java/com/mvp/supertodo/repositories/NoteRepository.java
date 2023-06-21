package com.mvp.supertodo.repositories;

import java.time.*;
import java.util.*;

import com.mvp.supertodo.entits.*;
import jakarta.persistence.*;
import lombok.*;
import org.springframework.stereotype.*;
import org.springframework.transaction.annotation.*;

@Repository
public class NoteRepository {

    @PersistenceContext
    private EntityManager entityManager;

    public Note findById(@NonNull Long id) {
        Note result = (Note) entityManager
            .createNativeQuery(
                String.format(
                    """
                       SELECT note.* FROM note
                       WHERE id = %d
                    """,
                    id
                ),
                Note.class
            ).getSingleResult();
        entityManager.close();
        return result;
    }

    public List<Note> findAllWithSort(@NonNull String sort) {
        List<Note> result = (List<Note>) entityManager
            .createNativeQuery(
                String.format(
                    """
                       SELECT note.* FROM note
                       ORDER BY %s
                    """,
                    sort
                ),
                Note.class
            ).getResultList();
        entityManager.close();
        return result;
    }

    public List<Note> findAllWithFilterAndSort(@NonNull boolean isCompleted, @NonNull String sort) {
        List<Note> result = (List<Note>) entityManager
            .createNativeQuery(
                String.format(
                    """
                      SELECT note.* FROM note
                      JOIN custom_user ON note.custom_user_id = custom_user.id
                      WHERE note.is_completed = %s
                      ORDER BY %s
                    """,
                    isCompleted,
                    sort
                ),
                Note.class
            ).getResultList();
        entityManager.close();
        return result;
    }

    public List<Note> findAllByOwnerUsernameWithSort(@NonNull String username, @NonNull String sort) {
        List<Note> result = (List<Note>) entityManager
            .createNativeQuery(
                String.format(
                    """
                      SELECT note.* FROM note
                      JOIN custom_user ON note.custom_user_id = custom_user.id
                      WHERE custom_user.username = '%s'
                      ORDER BY %s
                    """,
                    username,
                    sort
                ),
                Note.class
            ).getResultList();
        entityManager.close();
        return result;
    }

    public List<Note> findAllByOwnerUsernameWithFilterAndSort(
        @NonNull String username,
        @NonNull Boolean isCompleted,
        @NonNull String sort
    ) {
        List<Note> result = (List<Note>) entityManager
            .createNativeQuery(
                String.format(
                    """
                      SELECT note.* FROM note
                      JOIN custom_user ON note.custom_user_id = custom_user.id
                      WHERE custom_user.username = '%s' AND
                            note.is_completed = %s
                      ORDER BY %s
                    """,
                    username,
                    isCompleted,
                    sort
                ),
                Note.class
            ).getResultList();
        entityManager.close();
        return result;
    }

    @Transactional
    public void save(@NonNull Note note) {
        entityManager.persist(note);
    }

    @Transactional
    public void updateTextBodyByNoteId(@NonNull Long id, @NonNull String textBody) {
        entityManager
            .createNativeQuery(
                String.format(
                    """
                      UPDATE note SET text_body = '%s'
                      WHERE custom_user_id = %s
                    """,
                    textBody,
                    id
                )
            ).executeUpdate();
        entityManager.close();
    }

    @Transactional
    public Integer toggleCompletionStatusByNoteId(@NonNull Long id, @NonNull LocalDateTime completedAt) {
        Integer result = entityManager
            .createNativeQuery(
                String.format(
                    """
                      UPDATE note SET is_completed = (NOT is_completed),
                                      completed_at = cast('%s' AS timestamp)
                      WHERE id = %d
                    """,
                    completedAt,
                    id
                )
            ).executeUpdate();
        entityManager.close();
        return result;
    }

    @Transactional
    public void deleteNoteById(@NonNull Long id) {
        entityManager
            .createNativeQuery(
                String.format(
                    """
                      DELETE note WHERE id = %d
                    """,
                    id
                )
            ).executeUpdate();
        entityManager.close();
    }
}
