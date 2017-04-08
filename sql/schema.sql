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
     UNIQUE(status_id)
);

-- trumptweets.db


-- trumptweets mysql
CREATE DATABASE trumptweets CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE status (
    status_id varchar(36) NOT NULL,
    text varchar(255) NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (status_id)
) DEFAULT CHARSET=utf8;
