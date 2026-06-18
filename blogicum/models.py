import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "db.sqlite"
CREATE_TABLES_SQL = BASE_DIR / "create_tables.sql"

categories = [
    # (id, title)
    (1, "Наука"),
    (2, "Юмор"),
    (3, "Технологии"),
]

posts = [
    # (id, title, category_id, is_published, rating)
    (
        1,
        "10 лучших способов улучшить производительность вашего кода",
        3,
        True,
        4.5,
    ),
    (2, "Как создать свой первый проект на Python", 1, True, 3.3),
    (
        3,
        "10 важных принципов объектно-ориентированного программирования",
        3,
        True,
        4.8,
    ),
    (
        4,
        "Как использовать git для управления версиями вашего кода",
        3,
        True,
        4.2,
    ),
    (5, "Лучшие анекдоты про программистов", 2, True, 3.7),
    (
        6,
        "Как использовать алгоритмы для решения задач программирования",
        1,
        True,
        4.6,
    ),
    (
        7,
        "5 основных паттернов проектирования программного обеспечения",
        3,
        False,
        None,
    ),
    (
        8,
        "Как использовать Docker для управления окружением вашего приложения",
        3,
        False,
        None,
    ),
    (9, "Работа с базами данных в Python", 1, True, 4.1),
    (
        10,
        "Как создать свою первую игру на языке программирования C#",
        3,
        True,
        None,
    ),
]

authors = [
    # (id, username, first_name, second_name)
    (1, "petr_ivanov95", "Петр", "Кузнецов"),
    (2, "ann_smith", "Анна", "Смирнова"),
    (3, "max2010", "Максим", None),
    (4, "maria_777", "Мария", "Иванова"),
    (5, "alex_king", "Александр", None),
]

posts_authors = [
    # (post_id, author_id)
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 2),
    (3, 3),
    (4, 1),
    (4, 2),
    (5, 2),
    (6, 1),
    (6, 2),
    (6, 3),
    (7, 2),
    (8, 1),
    (9, 3),
    (10, 1),
    (10, 2),
]


def create_tables(cur: sqlite3.Cursor) -> None:
    """Создаёт таблицы, выполняя скрипт из create_tables.sql."""
    with open(CREATE_TABLES_SQL, encoding="utf-8") as sql_file:
        cur.executescript(sql_file.read())


def insert_data(cur: sqlite3.Cursor) -> None:
    """Наполняет таблицы исходными данными."""
    cur.executemany("INSERT INTO categories VALUES (?, ?);", categories)
    cur.executemany("INSERT INTO posts VALUES (?, ?, ?, ?, ?);", posts)
    cur.executemany("INSERT INTO authors VALUES (?, ?, ?, ?);", authors)
    cur.executemany("INSERT INTO posts__authors VALUES (?, ?);", posts_authors)


if __name__ == "__main__":
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    create_tables(cur)
    insert_data(cur)
    con.commit()
    con.close()
