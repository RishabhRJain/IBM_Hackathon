#!/usr/bin/env python

from flask import Flask
from flask import request
app = Flask(__name__)
@app.route('/login')
def hello_world():
    username = request.args.get(‘username’)
    return username
if __name__ == '__main__':
    app.run()