import pymysql
import os
from utils import get_count_from_cursor_execution


class UserResource:
    def __init__(self):
        pass

    @staticmethod
    def _get_connection():
        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn


    @staticmethod
    def createUser(userId, firstName, lastName, email):
        conn = UserResource._get_connection()
        cursor = conn.cursor()

        sql = """
        insert into PlaylistAccess.User
        values (%s, %s, %s, %s);
        """

        try:
            cursor.execute(sql, (userId, firstName, lastName, email))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def info():
        import pandas as pd
        conn = UserResource._get_connection()
        cursor = conn.cursor()

        sql = """
        select *
        from PlaylistAccess.User
        """

        try:
            cursor.execute(sql)
            r =cursor.fetchall()
            df = pd.DataFrame(r)
            print(df)
            cursor.close()
            return True
        except:
            return False

    @staticmethod
    def doesUserExist(userId):
        sql = """
        select count(*)
        from PlaylistAccess.User
        where id=%s;
        """

        conn = UserResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId))
            count = get_count_from_cursor_execution(cursor)
            cursor.close()
            return count != 0
        except:
            return False

    @staticmethod
    def _remove_user(userId):
        sql = """
        DELETE FROM PlaylistAccess.User WHERE id=%s;
        """

        conn = UserResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId))
            conn.commit()
        except:
            pass