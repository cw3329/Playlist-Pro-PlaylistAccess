import pymysql
import os


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


