import time
import sqlite3
import functools
from functools import lru_cache  # Alternative approach option

# Global cache dictionary
query_cache = {}

def cache_query(func):
    """Decorator that caches database query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Use the query as the cache key
        cache_key = query
        
        # Check if result is already cached
        if cache_key in query_cache:
            print("Returning cached result")
            return query_cache[cache_key]
        
        # Execute and cache if not in cache
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        print("Caching new result")
        return result
    return wrapper

@with_db_connection # type: ignore
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")