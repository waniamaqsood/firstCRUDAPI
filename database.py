import sqlite3


connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")


cursor.execute("""
    SELECT COUNT(*) FROM tasks
""")

count = cursor.fetchone()[0]


if count == 0:
    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [
            ("Learn SQLite", 0),
            ("Build a task API", 1),
            ("Test the application", 0)
        ]
    )


connection.commit()
connection.close()