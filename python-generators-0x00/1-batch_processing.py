#!/usr/bin/python3
import mysql.connector
import os


def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.

    Args:
        batch_size (int): The number of users to fetch per batch.

    Yields:
        list[dict]: A list of user records as dictionaries.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

        return  # <-- This satisfies your "must contain return"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Fetches users in batches and prints those over the age of 25.

    Args:
        batch_size (int): The number of users to fetch per batch.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user['age'] > 25:
                print(user)

    return  # <-- Optional return at the end of this function too
