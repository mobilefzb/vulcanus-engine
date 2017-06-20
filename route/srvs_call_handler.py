from __future__ import unicode_literals
from main import app
from flask import request



@app.route('/service_call', methods=['POST'])
def srvs_call():

    try:
        req = request
        req_data = yaml.load(req.data)

    except Exception as e:

       print e


