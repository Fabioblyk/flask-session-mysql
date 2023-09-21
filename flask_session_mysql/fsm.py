import json
import time
from uuid import uuid4
import mysql.connector
from flask.sessions import SessionInterface as FlaskSessionInterface
from flask.sessions import SessionMixin
from werkzeug.datastructures import CallbackDict
from flask import request, Flask


class ServerSideSession(CallbackDict, SessionMixin):
    """Baseclass for server-side based sessions."""

    def __init__(self, initial=None, sid=None, permanent=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        if permanent:
            self.permanent = permanent
        self.modified = False


class SessionInterface(FlaskSessionInterface):

    def _generate_sid(self):
        return str(uuid4())


class MysqlSessionInterface(SessionInterface):
    session_class = ServerSideSession

    def __init__(self, app: Flask, host, username, password, database, port):
        self.app = app
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port

    def _get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def open_session(self, app, request):
        sid = request.cookies.get(app.config["SESSION_COOKIE_NAME"])
        if not sid:
            sid = self._generate_sid()
            return self.session_class(sid=sid, permanent=self.session_class.permanent)

        db = self._get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT data FROM sessions WHERE session_id = %s', (sid,))

        res = cursor.fetchone()

        if res is None:
            sid = self._generate_sid()
            return self.session_class(sid=sid, permanent=self.session_class.permanent)

        data = json.loads(res['data'])

        if data:
            return self.session_class(dict(data), sid=sid)
        return self.session_class(sid=sid, permanent=self.session_class.permanent)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if not session:
            if session.modified:
                db = self._get_connection()
                cursor = db.cursor(dictionary=True)
                cursor.execute('DELETE FROM sessions WHERE session_id = %s', (session.sid,))
                db.commit()
                cursor.close()
                db.close()

                response.delete_cookie(app.config["SESSION_COOKIE_NAME"],
                                       domain=domain, path=path)
            return

        conditional_cookie_kwargs = {}
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        data = dict(session)

        db = self._get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT session_id FROM sessions WHERE session_id= %s ;', (session.sid,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `sessions` (`session_id`, `ip_address`, `data`, `user_agent`, `last_activity`)"
                           " VALUES (%s, %s, %s, %s, %s);",
                           (session.sid, request.remote_addr, json.dumps({}), request.user_agent.string, time.time()))

        else:
            cursor.execute(
                "UPDATE `sessions` SET `data` = %s, ip_address = %s, user_agent = %s  WHERE `sessions`.`session_id` = %s;",
                (json.dumps(data), request.remote_addr, request.user_agent.string, session.sid))

        db.commit()

        response.set_cookie(app.config["SESSION_COOKIE_NAME"], session.sid,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure,
                            **conditional_cookie_kwargs)
