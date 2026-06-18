def get_published_posts_count(cur) -> list[tuple]:
    # Напишите SQL запрос в строке.
    sql = """
    SELECT COUNT(*)
    FROM posts
    WHERE is_published = 1
      AND title LIKE 'Как%';
    """

    results = cur.execute(sql)
    return [row for row in results]


def get_top_5_posts(cur) -> list[tuple]:
    # Напишите SQL запрос в строке.
    sql = """
    SELECT *
    FROM posts
    ORDER BY rating DESC
    LIMIT 5;
    """
    results = cur.execute(sql)
    return [row for row in results]


def get_unique_authors(cur) -> list[tuple]:
    # Напишите SQL запрос в строке.
    sql = """
    SELECT DISTINCT authors.username
    FROM authors
    JOIN posts__authors ON authors.id = posts__authors.author_id
    ORDER BY authors.username;
    """

    results = cur.execute(sql)
    return [row for row in results]


def get_category_avg_rating(cur) -> list[tuple]:
    # Напишите SQL запрос в строке.
    sql = """
    SELECT categories.title,
           AVG(posts.rating)
    FROM categories
    JOIN posts ON categories.id = posts.category_id
    GROUP BY categories.id
    HAVING AVG(posts.rating) >= 4
    ORDER BY AVG(posts.rating) DESC;
    """
    results = cur.execute(sql)
    return [row for row in results]


def get_users_posts(cur) -> list[tuple]:
    # Напишите SQL запрос в строке.
    sql = """
    SELECT authors.second_name,
           authors.first_name,
           posts.title
    FROM authors
    LEFT JOIN posts__authors ON authors.id = posts__authors.author_id
    LEFT JOIN posts ON posts__authors.post_id = posts.id
    WHERE authors.second_name IS NOT NULL
    ORDER BY authors.second_name,
             authors.first_name,
             posts.title;
    """
    results = cur.execute(sql)
    return [row for row in results]
