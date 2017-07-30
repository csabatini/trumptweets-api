-- trumpwip.db

CREATE TABLE seed_quote (
     quote_id TEXT NOT NULL PRIMARY KEY,
     value TEXT NOT NULL,
     UNIQUE(quote_id)
);

CREATE TABLE quote_word (
     word TEXT NOT NULL PRIMARY KEY,
     UNIQUE(word)
);

CREATE TABLE status (
     status_id TEXT NOT NULL PRIMARY KEY,
     tags TEXT NOT NULL,
     UNIQUE(status_id)
);

CREATE TABLE status_v2 (
     status_id TEXT NOT NULL PRIMARY KEY,
     tags TEXT NULL,
     UNIQUE(status_id)
);

-- trumptweets.db
CREATE TABLE user_profile (
     guid TEXT NULL,
     push_enabled INTEGER NOT NULL,
     device_token TEXT NULL,
     UNIQUE(guid)
);
--INSERT INTO user_profile (push_enabled) VALUES (1);

CREATE TABLE status (
     status_id TEXT NOT NULL PRIMARY KEY,
     text TEXT NOT NULL,
     media_url TEXT NULL,
     created_at INTEGER NOT NULL,
     UNIQUE(status_id)
);

CREATE TABLE tag (
     tag_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     tag TEXT NOT NULL,
     UNIQUE(tag_id)
);

CREATE TABLE status_tag (
     status_tag_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     status_id TEXT NOT NULL,
     tag_id INTEGER NOT NULL,
     FOREIGN KEY (status_id) REFERENCES status(status_id),
     FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
     UNIQUE(status_id, tag_id)
);

CREATE TABLE favorite (
     status_id TEXT NOT NULL,
     FOREIGN KEY (status_id) REFERENCES status(status_id),
     UNIQUE(status_id)
);

-- trumptweets mysql
CREATE DATABASE trumptweets CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE user_profile (
    guid varchar(36) NOT NULL,
    push_enabled boolean NOT NULL,
    device_token varchar(200) NULL,
    created_time timestamp DEFAULT CURRENT_TIMESTAMP,
    status_max_created_at timestamp NULL DEFAULT NULL,
    PRIMARY KEY (guid)
) DEFAULT CHARSET=utf8;

-- temporary
CREATE TABLE status_word (
    status_word_id int NOT NULL AUTO_INCREMENT,
    word varchar(20) NOT NULL,
    PRIMARY KEY (status_word_id )
) DEFAULT CHARSET=utf8;

CREATE TABLE status (
    status_id varchar(36) NOT NULL,
    text varchar(255) NOT NULL,
    media_url varchar(100) NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (status_id)
) DEFAULT CHARSET=utf8;

CREATE TABLE tag (
    tag_id int NOT NULL AUTO_INCREMENT,
    tag varchar(25) NOT NULL,
    PRIMARY KEY (tag_id)
) DEFAULT CHARSET=utf8;

CREATE TABLE tag_alias (
    tag_alias_id int NOT NULL AUTO_INCREMENT,
    tag_id int NOT NULL,
    tag_alias varchar(25) NOT NULL,
    PRIMARY KEY (tag_alias_id),
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id)
) DEFAULT CHARSET=utf8;

CREATE TABLE status_tag (
    status_tag_id int NOT NULL AUTO_INCREMENT,
    status_id varchar(36) NOT NULL,
    tag_id int NOT NULL,
    PRIMARY KEY (status_tag_id),
    UNIQUE KEY ix_status_tag (status_id, tag_id),
    FOREIGN KEY (status_id) REFERENCES status(status_id),
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id)
) DEFAULT CHARSET=utf8;

CREATE TABLE user_notification (
    user_notification_id bigint NOT NULL AUTO_INCREMENT,
    user_guid varchar(36) NOT NULL,
    message varchar(100) NOT NULL,
    created_time timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_notification_id),
    FOREIGN KEY (user_guid) REFERENCES user_profile(guid)
);

ALTER TABLE user_notification ADD INDEX ix_user_notification_time (user_guid, created_time);

CREATE VIEW vw_tag_count_max_created AS
(
    SELECT tag.*, CASE WHEN count(*) < 100 THEN count(*) ELSE 100 END AS count, MAX(status.created_at) max_created_at
    FROM tag INNER JOIN status_tag
    ON tag.tag_id = status_tag.tag_id INNER JOIN status
    ON status_tag.status_id = status.status_id
    GROUP BY tag.tag_id, tag.tag
    ORDER BY 4 DESC
);
