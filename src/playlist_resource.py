import pymysql
import os
from utils import get_count_from_cursor_execution

class PlaylistResource:
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
    def createPlaylist(playlistId, name):
        sql = """
        insert into PlaylistAccess.Playlist
        values (%s, %s);
        """

        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (playlistId, name))
            conn.commit()
            return True
        #@TODO - remove debug print
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def doesPlaylistExist(playlistId):
        sql = """
        select count(*)
        from PlaylistAccess.Playlist
        where id=%s;
        """

        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (playlistId))
            count = get_count_from_cursor_execution(cursor)
            cursor.close()
            return count != 0
        except:
            return False

    @staticmethod
    def info():
        import pandas as pd
        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()

        sql = """
                select *
                from PlaylistAccess.Playlist
                """

        try:
            cursor.execute(sql)
            r = cursor.fetchall()
            df = pd.DataFrame(r)
            print(df)
            cursor.close()
            return True
        except:
            return False