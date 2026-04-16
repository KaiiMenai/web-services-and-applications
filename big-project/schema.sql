DROP TABLE IF EXISTS task;
create table task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "Task Name" VARCHAR(50) NOT NULL,
    "Description" VARCHAR(250),
    "Due Date" DATE
);