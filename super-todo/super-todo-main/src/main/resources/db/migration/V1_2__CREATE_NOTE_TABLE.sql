CREATE TABLE Note
(
    id             BIGINT AUTO_INCREMENT NOT NULL,
    title          VARCHAR(255),
    link           TEXT,
    text_body       TEXT,
    timestamp      TIMESTAMP,
    completed_at    TIMESTAMP,
    custom_user_id BIGINT,
    is_completed    BOOLEAN,
    CONSTRAINT pk_note PRIMARY KEY (id)
);

ALTER TABLE Note
    ADD CONSTRAINT FK_NOTE_ON_CUSTOM_USER FOREIGN KEY (custom_user_id) REFERENCES custom_user (id);