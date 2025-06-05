DROP TABLE IF EXISTS Password;

CREATE TABLE Password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Servizio TEXT,
    Nickname TEXT,
    Email TEXT,
    Passkey TEXT
);