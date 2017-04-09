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
     tags TEXT NOT NULL
     UNIQUE(status_id)
);

-- trumptweets.db
CREATE TABLE status (
     status_id TEXT NOT NULL PRIMARY KEY,
     text TEXT NOT NULL,
     created_at INTEGER NOT NULL,
     UNIQUE(status_id)
);

CREATE TABLE tag (
     tag_id INTEGER NOT NULL PRIMARY KEY,
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

-- trumptweets mysql
CREATE DATABASE trumptweets CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE status (
    status_id varchar(36) NOT NULL,
    text varchar(255) NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (status_id)
) DEFAULT CHARSET=utf8;

CREATE TABLE tag (
    tag_id int NOT NULL AUTO_INCREMENT,
    tag varchar(25) NOT NULL,
    PRIMARY KEY (tag_id)
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
