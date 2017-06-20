from __future__ import unicode_literals
from main import app
import traceback
from flask import request


@app.route('/test', methods=['GET', 'POST'])
def index():
    try:
        if request.method == "GET":
            return '<h1>Wellcome To Vulcanus-Engine</h1>'
        else:
            return '<h1>Not Support This Method</h1>'
    except Exception as e:
        exstr = traceback.format_exc()