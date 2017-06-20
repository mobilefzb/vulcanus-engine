from __future__ import unicode_literals
from main import app
from flask import request
import yaml
from settings import ETCD_HOST, ETCD_PORT
from validator.reqdata_validate import basic_validate, namespace_validate
from registry_controller.namespace_controller import NamespaceController


@app.route('/namespace', methods=['POST'])
def namespace_create():

    try:

        req = request
        req_data = yaml.load(req.data)

        #   validata the request data
        basic_validate(req_data)
        namespace_validate(req_data)

        #   record the ns
        controller = NamespaceController(ETCD_HOST, ETCD_PORT)
        controller.write_namespace(req_data)

    except Exception as e:

       print e


@app.route('/namespace/<ns_name>', methods=["GET"])
def namespace_get(ns_name):

    try:

        # TODO  validata the ns_name exit?
        controller = NamespaceController(ETCD_HOST, ETCD_PORT)
        data = controller.get_namespace(ns_name)

        return data

    except Exception as e:

        print e


@app.route('/namespace/<ns_name>', methods=["DELETE"])
def namespace_delete(ns_name):

    try:

        controller = NamespaceController(ETCD_HOST, ETCD_PORT)
        controller.delete_namespace(ns_name)

    except Exception as e:

        print e