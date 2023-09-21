from .fsm import MysqlSessionInterface
from flask import Flask
import mysql.connector


class MysqlSession(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """This is used to set up session for your app object.

        :param app: the Flask app object with proper configuration.
        """
        app.session_interface = self.mysql_interface(app)
        return

    def mysql_interface(self, app: Flask):
        table = """CREATE TABLE IF NOT EXISTS `sessions` (
        `session_id` VARCHAR(64),
        `ip_address` TEXT,
        `data` TEXT,
        `user_agent` TEXT,
        `last_activity` TEXT,
        PRIMARY KEY (`session_id`)
    );"""
        config = app.config.copy()
        config.setdefault('MYSQL_SESSION_HOST', None)
        config.setdefault('MYSQL_SESSION_USERNAME', None)
        config.setdefault('MYSQL_SESSION_PASSWORD', None)
        config.setdefault('MYSQL_SESSION_DATABASE', None)
        config.setdefault('MYSQL_SESSION_PORT', 3306)

        conn = mysql.connector.connect(
            host=config['MYSQL_SESSION_HOST'],
            user=config['MYSQL_SESSION_USERNAME'],
            password=config['MYSQL_SESSION_PASSWORD'],
            database=config['MYSQL_SESSION_DATABASE'],
            port=config['MYSQL_SESSION_PORT']
        )
        cur = conn.cursor()
        cur.execute(table)

        return MysqlSessionInterface(
            app,
            config['MYSQL_SESSION_HOST'],
            config['MYSQL_SESSION_USERNAME'],
            config['MYSQL_SESSION_PASSWORD'],
            config['MYSQL_SESSION_DATABASE'],
            config['MYSQL_SESSION_PORT']

        )
