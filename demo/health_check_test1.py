import sys
import os
self_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(self_path), "drivers"))
import threading
import Queue
from Queue import Empty
import json
import time
import traceback
import daemon
import etcd3

from health_drivers.httpdriver import *
from health_drivers.rabbitmqdriver import *
from health_drivers.shellscriptdriver import *

def watch_etcd_event(key, watched_queue):
    client = etcd3.client()
    events_iterator, cancel = client.watch_prefix(key)
    try:
        for event in events_iterator:
            # help(event)
            print(getattr(event, "key"))
            print(getattr(event, "value"))
            # if 'key' in event and 'value' in event:
            # print event['kv']['key']
            # print event['kv']['value']
            check_flag = getattr(event, "key")
            pre_check_info_str = getattr(event, "value").replace("u'", '"').replace("'", '"').replace("True", "true")
            if check_flag and pre_check_info_str:
                watched_queue.put((check_flag, pre_check_info_str))
    except Exception as ex:
        print(traceback.format_exc())
        print(ex)

def trigger_watch(interval, watched_queue):
    count = 1
    watched_dict = {}
    client = etcd3.client()
    while True:
        try:
            if not watched_queue.empty():
                check_flag, pre_check_info_str = watched_queue.get()
                if check_flag not in watched_dict:
                    watched_dict[check_flag] = json.loads(pre_check_info_str)
            for k, pre_check_info in watched_dict.items():
                if pre_check_info['spec']['Driver'] == 'HTTPClient':
                    ret = check_http_service_health(pre_check_info['spec']['URL'])
                elif pre_check_info['spec']['Driver'] == 'RabbitMQClient':
                    ret = check_rabbitmq_service_health(pre_check_info['spec']['BrokerServerHost'])
                elif pre_check_info['spec']['Driver'] == 'ShellScriptClient':
                    host = pre_check_info['spec']['ServerHost']
                    usrname = pre_check_info['spec']['Username']
                    passwd = pre_check_info['spec']['Password']
                    keyword = pre_check_info['spec']['Cmd']
                    ret = check_remote_shell_script_health(keyword, usrname, passwd, host)
                else:
                    continue
                count += 1
                if not ret:
                    # delete key to notify others
                    print("%s dead!" % (k))
                    client.delete(k)
                    del watched_dict[k]
                else:
                    print("%s is ok!" % (k))
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)
        time.sleep(interval)

watched_queue = Queue.Queue()
threads = []
t1 = threading.Thread(target=watch_etcd_event, args=('/registry/endpoint', watched_queue))
t2 = threading.Thread(target=trigger_watch, args=(5, watched_queue))
threads.append(t1)
threads.append(t2)

if __name__ == '__main__':
    # with daemon.DaemonContext():
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
