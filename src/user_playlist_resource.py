import pymysql
import os

class UserPlaylistResource:
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
    def hasAccessToPlaylist(userId, playlistId):
        """
        :param userId: User ID for a specific user
        :param playlistId: Playlist ID
        :return: True if user has access, False otherwise
        """

        sql = """
        select count(*)
        from PlaylistAccess.UserPlaylist
        where userId=%s and playlistId=%s;
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId, playlistId))
            num_rows = cursor.fetchone()[0]
            return num_rows != 0
        except:
            return False

    @staticmethod
    def addUserToPlaylist(elevatedUserId, newUserId, playlistId):
        """
        elevateduserId grants permission for newUserId to add songs
        to playlist

        :param elevatedUserId: user ID of elevated user
        :param newUserId: new user ID being added
        :param playlistId: playlist ID
        :return: True if user is added, False otherwise
        """

        sql = """
        insert into PlaylistAccess.UserPlaylist (userId, playlistId)
        select %s, %s
        from PlaylistAccess.UserPlaylist
        where (
	        select count(*)
  	        from PlaylistAccess.UserPlaylist as UP
  	        where UP.userId=%s and UP.playlistId=%s
        ) = 1;
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (newUserId, playlistId, elevatedUserId, playlistId))
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def removeUserFromPlaylist(elevatedUserId, userIdToRemove, playlistId):
        """
        Attempts to remove a user from a playlist

        :param elevatedUserId: user ID for elevated user
        :param userIdToRemove: user ID that will be removed
        :param playlistId: playlist ID
        :return: True if the user can and is removed, False otherwise
        """

        sql = """
        DELETE u.*
        FROM PlaylistAccess.UserPlaylist u
        where u.userId=%s and u.playlistId=%s and
        (
            select count(*)
            from (
              select * from
              PlaylistAccess.UserPlaylist as UP
              where UP.userId=%s and UP.playlistId=%s
            ) as x
        ) = 1;
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userIdToRemove, playlistId, elevatedUserId, playlistId))
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def createPlaylistForUser(userId, playlistId):
        """
        Creates a playlist for a user. This is creating the shared "UserPlaylist" table
        from an existing userId and existing playlistId

        :param userId: user ID to create for
        :param playlistId: playlist ID
        :return: True if successful, False otherwise
        """

        sql = """
        insert into PlaylistAccess.UserPlaylist
        select %s, %s
        from PlaylistAccess.UserPlaylist
        where (
	        select count(*)
  	        from PlaylistAccess.UserPlaylist as UP
  	        where UP.playlistId=%s
        ) = 0;
        """

        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (userId, playlistId, playlistId))
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def info():
        import pandas as pd
        conn = UserPlaylistResource._get_connection()
        cursor = conn.cursor()

        sql = """
            select *
            from PlaylistAccess.UserPlaylist
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



