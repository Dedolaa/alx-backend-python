import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Run both queries concurrently"""
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

def main():
    """Run the concurrent fetch and print results"""
    all_users, older_users = asyncio.run(fetch_concurrently())
    
    print("\nAll Users:")
    for user in all_users:
        print(user)
    
    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    main()