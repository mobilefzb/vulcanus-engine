from __future__ import unicode_literals
from main import app
from flask import request
import yaml
from settings import ETCD_HOST, ETCD_PORT
from validator.reqdata_validate import basic_validate, srvs_register_validate
from registry_controller.srvs_register_controller import SrvsRegisterController


@app.route('/service', methods=['POST'])
def service_create():

    try:

        req = request
        req_data = yaml.load(req.data)

        #   validata the request data
        basic_validate(req_data)
        srvs_register_validate(req_data)

        #   record the ns
        controller = SrvsRegisterController(ETCD_HOST, ETCD_PORT)
        controller.write_srvs(req_data)

    except Exception as e:
       print e


@app.route('/service/<srv_name>', methods=["GET"])
def service_get(srv_name):

    try:

        # TODO  validata the ns_name exit?
        controller = SrvsRegisterController(ETCD_HOST, ETCD_PORT)
        data = controller.get_srvs(srv_name)

        return data

    except Exception as e:
        pass


@app.route('/service/<srv_name>', methods=["DELETE"])
def service_delete(srv_name):

    try:

        controller = SrvsRegisterController(ETCD_HOST, ETCD_PORT)
        controller.delete_srvs(srv_name)

    except Exception as e:

        pass
