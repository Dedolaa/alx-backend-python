#!/usr/bin/python3
import seed

def stream_user_ages():
    """
    Generator that streams user ages from the user_data table one by one.
    Yields:
        int: age of a user
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age of all users using a generator to stream data.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
