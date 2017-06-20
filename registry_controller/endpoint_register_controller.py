from registry_center.client import Register
from registry_controller import rs_store_dir
import threading
import os
import json
threads = []


class EndPointRegisterController(object):

    def __init__(self, req_host, req_port):

        self.__client = Register(req_host, req_port)

    def watch_srvs_endpoint(self):

        def watch_etcd_event():
            client = self.__client.get_client()
            events_iterator, cancel = client.watch_prefix(rs_store_dir.get("Service"))
            for event in events_iterator:

                print event['kv']['key']
                print event['kv']['value']
                data = (event['kv']['value']).encode("gbk")
                print type(data)
                req_data = json.loads(data)
                endpoint_payload = dict()

                endpoint_payload["apiVersion"] = req_data.get("apiVersion")
                endpoint_payload["kind"] = "EndPoint"
                endpoint_payload["metadata"] = req_data.get("metadata")
                endpoint_payload["spec"] = req_data.get("spec").get("input").get("BasicInfos")

                client.put(os.path.join(rs_store_dir.get("EndPoint"), os.path.basename(event['kv']['key'])), endpoint_payload)

        try:

            t1 = threading.Thread(target=watch_etcd_event)
            threads.append(t1)

            for t in threads:
                t.setDaemon(True)
                t.start()
                t.join()

        except Exception as e:

            pass

    def delete_endpoint(self, srvs_name):

        try:

            self.__client.delete_vaule(srvs_name)

        except Exception as e:

            raise

if __name__ == '__main__':


    edc = EndPointRegisterController("localhost", 2379)

    edc.watch_srvs_endpoint()
