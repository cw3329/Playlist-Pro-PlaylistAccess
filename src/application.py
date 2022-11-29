from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from user_playlist_resource import UserPlaylistResource
from user_resource import UserResource
from playlist_resource import PlaylistResource
from flask_cors import CORS

__VERSION__ = '1.1' # For testing

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "PlaylistAccess Microservice",
        "health": "Good",
        "at time": t,
        "version": __VERSION__
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@app.route("/api/playlistaccess/<playlistId>/access/<userId>", methods=["GET"])
def hasAccessToPlaylist(userId, playlistId):
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.hasAccessToPlaylist(userId, playlistId)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")

    return rsp

@app.route("/api/playlistaccess/<playlistId>/user/<userId>/add/<newUserId>", methods=["POST"])
def addUserToPlaylist(playlistId, userId, newUserId):
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.addUserToPlaylist(userId, newUserId, playlistId)
    rsp = Response(json.dumps(f"{userId} adding {newUserId} to {playlistId}: {'success' if res else 'failure'}"),
                   status=201, content_type="text/plain")

    return rsp


@app.route("/api/playlistaccess/<playlistId>/user/<userId>/remove/<userIdToRemove>", methods=["DELETE"])
def removeUserFromPlaylist(playlistId, userId, userIdToRemove):
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.removeUserFromPlaylist(userId, userIdToRemove, playlistId)
    rsp = Response(json.dumps(f"{userId} removing {userIdToRemove} to {playlistId}: {'success' if res else 'failure'}"),
                   status=201, content_type="text/plain")

    return rsp

@app.route("/api/playlistaccess/<playlistId>/create/<userId>", methods=["POST"])
def createPlaylistForUser(playlistId, userId):
    request_inputs = rest_utils.RESTContext(request)

    print(request_inputs.args)

    res = UserPlaylistResource.createPlaylistForUser(userId, playlistId, request_inputs.args)
    rsp = Response(json.dumps(f"{'success' if res else 'failure'}"),
                   status=201, content_type="text/plain")
    return rsp

@app.route("/api/user/info", methods=["GET"])
def dbgUser():
    request_inputs = rest_utils.RESTContext(request)

    res = UserResource.info()
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route("/api/playlistaccess/info", methods=["GET"])
def dbgUserPlaylist():
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.info()
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route("/api/playlist/info", methods=["GET"])
def dbgPlaylist():
    request_inputs = rest_utils.RESTContext(request)

    res = PlaylistResource.info()
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

if __name__ == '__main__':
    # @TODO: remove the test db at some point
    # import os
    # import pymysql
    # import os
    # usr = os.environ.get("DBUSER")
    # pw = os.environ.get("DBPW")
    # h = os.environ.get("DBHOST")
    # print(usr, h)
    # conn = pymysql.connect(
    #     user=usr,
    #     password=pw,
    #     host=h,
    #     cursorclass=pymysql.cursors.DictCursor,
    #     autocommit=True
    # )
    # cursor = conn.cursor()
    # with open("test_db.sql", "r") as f:
    #     lines = f.read().split(";")[:-1]
    # for i, req in enumerate(lines):
    #     req += ";"
    #     print(req)
    #     cursor.execute(req)
    # Force change
    app.run(host="0.0.0.0", port=5011)