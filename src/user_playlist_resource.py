import pymysql
import os

from utils import get_count_from_cursor_execution
from user_resource import UserResource
from playlist_resource import PlaylistResource

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
            num_rows = get_count_from_cursor_execution(cursor)
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
    def createPlaylistForUser(userId, playlistId, kwargs):
        """
        Creates a playlist for a user. This is creating the shared "UserPlaylist" table.

        If the userId doesn't exist yet you can provide arguments:
            firstName, lastName, email

        If the playlistId doesn't exist yet you can provide arguments:
            playlistName

        :param userId: user ID to create for
        :param playlistId: playlist ID
        :param kwargs: dictionary of arguments
        :return: True if successful, False otherwise
        """

        user_required_args = ['firstName', 'lastName', 'email']
        playlist_required_args = ['playlistName']
        required_args = set()
        user_exists = playlist_exists = True

        if not UserResource.doesUserExist(userId):
            user_exists = False
            required_args |= set(user_required_args)
        if not PlaylistResource.doesPlaylistExist(playlistId):
            playlist_exists = False
            required_args |= set(playlist_required_args)

        # Make sure the required arguments were passed
        if not all(key in set(kwargs.keys()) for key in required_args):
            return False

        try:
            if not user_exists:
                if not UserResource.createUser(userId, *list(map(kwargs.get, user_required_args))):
                    return False
        except:
            return False  # May happen if there aren't proper args
        try:
            if not playlist_exists:
                if not PlaylistResource.createPlaylist(playlistId, *list(map(kwargs.get, playlist_required_args))):
                    UserResource._remove_user(userId)
                    return False
        except:
            return False  # May happen if there aren't proper args


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
            print(r)
            cursor.close()
            return r
        except:
            return False
