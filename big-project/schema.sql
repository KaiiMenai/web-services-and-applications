DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE category (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(50) NOT NULL,
    user_id    INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE task (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name   VARCHAR(50)  NOT NULL,
    description VARCHAR(250),
    due_date    DATE,
    status      VARCHAR(20)  DEFAULT 'pending',
    category_id INTEGER,
    user_id     INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (user_id)     REFERENCES user(id)
);

-- https://www.sqlite.org/foreignkeys.html; https://www.sqlite.org/datatype3.html