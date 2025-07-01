#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily paginates users from the database.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list[dict]: A page of users (as dictionaries).
    """
    offset = 0
    while True:  # Only one loop used
        page = paginate_users(page_size, offset)
        if not page:
            return  # Stop iteration when no more data
        yield page
        offset += page_size
