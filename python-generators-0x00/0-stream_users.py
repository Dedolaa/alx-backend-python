#!/usr/bin/python3
import mysql.connector
import os

def stream_users():
    """
    Generator function that connects to the ALX_prodev database and streams users one by one.
    Yields:
        dict: a dictionary containing user_id, name, email, and age
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # So we get dicts instead of tuples

        # Execute query to select all users
        cursor.execute("SELECT * FROM user_data")

        # Yield each row one at a time
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
