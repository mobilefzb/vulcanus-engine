import os
from . import rs_store_dir
from registry_center.client import Register
import json


class NamespaceController(object):

    def __init__(self, req_host, req_port):

        self.__client = Register(req_host, req_port)

    def write_namespace(self, req_data):

        try:

            ns_name = req_data.get("metadata").get("name")
            store_key = os.path.join(rs_store_dir.get("Namespace"), ns_name)
            self.__client.put_value(store_key, json.dumps(req_data))

        except Exception as e:

            raise

    def get_namespace(self, ns_name):

        try:

            store_key = os.path.join(rs_store_dir.get("Namespace"), ns_name)
            ns_detail = self.__client.get_value(store_key)

            return json.dumps(ns_detail[0])

        except Exception as e:
            raise

    def delete_namespace(self, ns_name):

        try:

            store_key = os.path.join(rs_store_dir.get("Namespace"), ns_name)

            self.__client.delete_vaule(store_key)

        except Exception as e:

            raise
