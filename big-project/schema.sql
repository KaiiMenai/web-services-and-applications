DROP TABLE IF EXISTS task;
CREATE TABLE task (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name   VARCHAR(50) NOT NULL,
    description VARCHAR(250),
    due_date    DATE
);