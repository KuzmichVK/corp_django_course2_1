-- Пересоздаём таблицы с нуля: DROP в обратном порядке зависимостей,
-- CREATE — в прямом. Делает скрипт идемпотентным (повторный запуск
-- models.py не плодит дубли).

DROP TABLE IF EXISTS posts__authors;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS categories;

-- Тематические категории
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

-- Авторы публикаций
CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,   -- никнейм обязателен и уникален
    first_name TEXT NOT NULL,
    second_name TEXT                 -- фамилия необязательна (может быть NULL)
);

-- Публикации
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category_id INTEGER NOT NULL,    -- категория обязательна
    is_published INTEGER NOT NULL,   -- булево: в SQLite хранится как 0/1
    rating REAL,                     -- дробное; может быть NULL (ещё не оценён)
    FOREIGN KEY (category_id) REFERENCES categories (id)   -- связь M:1
);

-- Связка публикация <-> автор (многие-ко-многим)
CREATE TABLE posts__authors (
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, author_id),                       -- композитный PK
    FOREIGN KEY (post_id) REFERENCES posts (id),
    FOREIGN KEY (author_id) REFERENCES authors (id)
);
