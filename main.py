from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.secret_key = app.config['SECRET_KEY']
app.permanent_session_lifetime = timedelta(minutes=30)

import route

if __name__ == '__main__':
    app.run()

