
from pymysql import connect
from pymysql.cursors import DictCursor


class Database:
    def __init__(self):
        self.connection = connect(
            host="localhost",
            user="root",
            password="******",
            database="intern",
            cursorclass=DictCursor
        )

    def viewid(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE user_id = %s",
                (user_id,)
            )
            return cursor.fetchone()

    def add_user(self, user):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO users (user_name, password_hash)
                   VALUES (%s, %s)""",
                user
            )
        self.connection.commit()

    def close(self):
        self.connection.close()

    def get_user_by_username(self, user_name):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT user_id, user_name, password_hash
                   FROM users
                   WHERE user_name = %s""",
                (user_name,)
            )
        return cursor.fetchone()