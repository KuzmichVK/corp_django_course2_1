# Changelog — corp_django_course2_1 (Блогикум: БД и CRUD)

Проверочная работа курса «Работа с базами данных в Django».
Все 15 тестов проходят (`uv run pytest` из корня репо).

## Окружение
- `uv venv` (CPython 3.12) → `.venv`
- `uv pip install -r requirements.txt` (pytest 7.2.2 + зависимости; Django и flake8 в этом репо нет)
- Все команды через `uv run`

## Изменения по файлам

### blogicum/create_tables.sql — НОВЫЙ
SQL-скрипт создания 4 таблиц по схеме БД:
- `categories` (id PK, title NOT NULL)
- `authors` (id PK, username NOT NULL UNIQUE, first_name NOT NULL, second_name nullable)
- `posts` (id PK, title, category_id NOT NULL → FK categories, is_published, rating nullable)
- `posts__authors` — связка M:M (post_id, author_id), композитный PK + два FK
- Идемпотентность: `DROP TABLE IF EXISTS` (обратный порядок зависимостей) перед `CREATE`,
  поэтому повторный запуск models.py не плодит дубли.

### blogicum/models.py — переписан с заготовки
- Пути через pathlib: `DATABASE = blogicum/db.sqlite`, `CREATE_TABLES_SQL = blogicum/create_tables.sql`
- Списки данных: `categories`, `posts`, `authors`, `posts_authors` (дословно по заданию)
- `create_tables(cur)` — читает create_tables.sql и выполняет через `executescript`
- `insert_data(cur)` — `executemany` для всех 4 таблиц (параметризация `?`)
- `__main__`: connect → create_tables → insert_data → commit → close

### blogicum/crud.py — заполнены 5 SQL-запросов
- `get_published_posts_count` — COUNT(*), WHERE is_published = 1 AND title LIKE 'Как%' → [(4,)]
- `get_top_5_posts` — SELECT *, ORDER BY rating DESC, LIMIT 5
- `get_unique_authors` — DISTINCT username, JOIN posts__authors, ORDER BY username
- `get_category_avg_rating` — AVG(rating), GROUP BY category, HAVING AVG >= 4, ORDER BY AVG DESC
- `get_users_posts` — LEFT JOIN (авторы без постов остаются, title=NULL),
  WHERE second_name IS NOT NULL, ORDER BY second_name, first_name, title

## Нюансы / решения
- БД называется `db.sqlite` (не `db.sqlite3`) — этого требует conftest.py; файл в .gitignore, в репо не коммитится
- Таблица `posts__authors` (двойное подчёркивание), переменная `posts_authors` (одинарное) — тесты различают
- `is_published = 1`, а не `= True` — 1 это фактическое хранение булева в SQLite, надёжнее литерала
- PRAGMA foreign_keys не включается: порядок вставки корректен, целостность тесты не проверяют
- E501 на длинных заголовках в списке posts — это данные (идентичны conftest Практикума), не код; на pytest не влияет

## Грабли (на будущее)
- При первом прогоне БД была пустой → 13 падений с `no such table` / `has no attribute`.
  Причина: models.py не был сохранён перед `uv run python blogicum/models.py`.
  Урок: сохранить файлы ПЕРЕД генерацией db.sqlite и прогоном pytest.
