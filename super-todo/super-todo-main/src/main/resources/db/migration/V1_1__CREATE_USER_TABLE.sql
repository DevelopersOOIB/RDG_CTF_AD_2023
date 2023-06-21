CREATE TABLE custom_user
(
    id       BIGINT AUTO_INCREMENT NOT NULL,
    username VARCHAR(252),
    password VARCHAR(255),
    is_admin BOOLEAN,
    CONSTRAINT pk_custom_user PRIMARY KEY (id)
);

ALTER TABLE custom_user
    ADD CONSTRAINT uc_custom_user_username UNIQUE (username);