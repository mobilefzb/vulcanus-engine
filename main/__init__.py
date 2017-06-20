# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
import route

@app.before_request
def before_request():

    pass