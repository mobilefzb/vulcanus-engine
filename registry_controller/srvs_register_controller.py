import os
from . import rs_store_dir
from registry_center.client import Register
import json
from error.etcd_exception import EtcdError


class SrvsRegisterController(object):

    def __init__(self, req_host, req_port):

        self.__client = Register(req_host, req_port)

    def write_srvs(self, req_data):

        try:

            #   store the service
            srvs_name = req_data.get("metadata").get("name")
            store_key = os.path.join(rs_store_dir.get("Service"), srvs_name)
            if not self.__client.put_value(store_key, json.dumps(req_data)):

                raise EtcdError("regist %s service faild!" % srvs_name)

        except Exception as e:

            raise

    def get_srvs(self, srvs_name):

        try:

            store_key = os.path.join(rs_store_dir.get("Service"), srvs_name)
            ns_detail = self.__client.get_value(store_key)

            return json.dumps(ns_detail[0])

        except Exception as e:
            raise

    def delete_srvs(self, srvs_name):

        try:

            store_key = os.path.join(rs_store_dir.get("Service"), srvs_name)

            if not self.__client.delete_vaule(store_key):

                raise EtcdError("delete %s service faild" % srvs_name)

        except Exception as e:

            raise
