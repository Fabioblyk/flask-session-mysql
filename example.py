from flask import Flask, session
from flask_session_mysql import MysqlSession

app = Flask(__name__)
app.secret_key = 'some_pretty_cool_secret_key_here'
app.config['MYSQL_SESSION_HOST'] = 'localhost'
app.config['MYSQL_SESSION_USERNAME'] = 'root'
app.config['MYSQL_SESSION_PASSWORD'] = ''
app.config['MYSQL_SESSION_DATABASE'] = 'test'

MysqlSession(app)


@app.route('/example')
def example():
    session['hello'] = 'world'
    return "Hello World"


app.run(port=5555)
