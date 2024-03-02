import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# CRUD + S
# CRUD
# CUD / R -> W / R
def execute_write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully for write")
    except Error as e:
        print(f"The error '{e}' occurred for write")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred for read")


conn = create_connection("test02.db")
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  nationality TEXT
);
"""
execute_write_query(conn, create_users_table)
create_users = """
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""


def read_users(connection):
    print("READ USERS")
    select_users = "SELECT * from users;"
    users = execute_read_query(connection, select_users)
    for user in users:
        print(user)
    print("\n")


execute_write_query(conn, create_users)
read_users(conn)
# update
update_user_nationality = """
UPDATE
  users
SET
  nationality = "China"
WHERE
  nationality <> "China"
"""

execute_write_query(conn, update_user_nationality)
read_users(conn)

# delete
delete_user = "DELETE FROM users WHERE id = 5"
execute_write_query(conn, delete_user)
read_users(conn)


