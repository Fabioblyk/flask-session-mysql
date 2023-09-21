# Flask Session MySQL

Flask-session-mysql is a package that enhances the security and usability of Flask sessions by storing them in a MySQL database. This server-side storage ensures that no sensitive data is exposed, prioritizing security.

# How it Works

The functioning of this package is straightforward. When a session is generated or data is stored (in cookies), Flask typically stores this information in a base64-encoded format within the browser's session cookies. However, this approach can be both vulnerable and unsafe.

To enhance security, this package generates a unique 64-character UUID (Universally Unique Identifier) code. This ensures that the cookies used for sessions are both secure and resistant to vulnerabilities, significantly improving the overall security of your application and making your life easier.


### Flask approach

![Flask_approach](https://github.com/Fabioblyk/flask-session-mysql/blob/master/images/flask_approach.png?raw=true)

Which if you decode 

**eyJoZWxsbyI6IndvcmxkIn0.ZQxasQ.KgRPUWvqZ57ccAWwd9qzOdAa9dg ---> {"hello":"world"}C@=E{qj@k`** (Pretty unsafe)

### Flask Session MySQL approach

![My_Approach](https://github.com/Fabioblyk/flask-session-mysql/blob/master/images/flask_session_mysql_approach.png?raw=true)
![db_table](https://github.com/Fabioblyk/flask-session-mysql/blob/master/images/db_image.png?raw=true)

As you see this is more secure and better for production development feel free to report any issues or suggestions!

## INSTALLATION

```shell
pip install flask-session-mysql
```
or with git

```shell
git clone https://github.com/Fabioblyk/flask-session-mysql
python setup.py install
```

How to use it?

```python
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
```
**NOTE**: Make sure you config the mysql data before bind it with MysqlSession(app) is it won't work
First configuration then binding!

