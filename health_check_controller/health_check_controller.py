import sys
import os
self_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(self_path), "drivers"))
import Queue
from Queue import Empty
import threading
from multiprocessing.dummy import Pool as ThreadPool
import json
import time
import traceback
import daemon
import etcd3

from health_drivers.health_drivers_log import init, info, warn, error, debug
from health_drivers.health_drivers_map import DRIVER_MAP

LOGGER_NAME = "healthcheck"

WATCH_FLAG = "/registry/endpoint"
CHECK_INTERVAL = 5

def watch_etcd_event(key, watched_queue):
    client = etcd3.client()
    events_iterator, cancel = client.watch_prefix(key)
    try:
        for event in events_iterator:
            debug(getattr(event, "key"))
            debug(getattr(event, "value"))
            check_flag = getattr(event, "key")
            pre_check_info_str = getattr(event, "value").replace("u'", '"').replace("'", '"').replace("True", "true")
            if check_flag and pre_check_info_str:
                watched_queue.put((check_flag, pre_check_info_str))
    except Exception as ex:
        error(traceback.format_exc())
        error(ex)
    sys.exit(1)

def watch_pool_management(interval, watched_queue):
    try:
        watched_dict = {}
        pool = ThreadPool(10)
        while True:
            if not watched_queue.empty():
                check_flag, pre_check_info_str = watched_queue.get()
                if check_flag not in watched_dict:
                    watched_dict[check_flag] = json.loads(pre_check_info_str)
            task_list = watched_dict.items()
            if task_list:
                # the purpose is just to make health check task
                # running concurrently in one check period
                # every check task should complete in one check
                # period
                # if there are some new watch tasks added in during
                # the check, they will be done at next period
                check_results = pool.map(trigger_watch, task_list)
                for check_result in check_results:
                    for chk_f, res in check_result.items():
                        if not res:
                            del watched_dict[chk_f]
            time.sleep(interval)
        pool.close()
        pool.join()
    except Exception as ex:
        error(traceback.format_exc())
        error(ex)

def trigger_watch(elem):
    health_ret = False
    try:
        check_flag, pre_check_info = elem
        ret = False
        driver_name = pre_check_info['spec']['Driver']
        if driver_name in DRIVER_MAP:
            chk_func = DRIVER_MAP[driver_name]
            ret = chk_func(pre_check_info['spec'])
        else:
            warn("Failed to find health check driver for %s." % (check_flag))
        if not ret:
            client = etcd3.client()
            # delete key to notify others
            info("%s dead!" % (check_flag))
            client.delete(check_flag)
            health_ret = False
        else:
            info("%s is ok!" % (check_flag))
            health_ret = True
    except Exception as ex:
        error(traceback.format_exc())
        error(ex)
    return {check_flag : health_ret}

if __name__ == '__main__':
    with daemon.DaemonContext():
        init(LOGGER_NAME)
        watched_queue = Queue.Queue()
        threads = []
        t1 = threading.Thread(target=watch_etcd_event, args=(WATCH_FLAG, watched_queue))
        t2 = threading.Thread(target=watch_pool_management, args=(CHECK_INTERVAL, watched_queue))
        threads.append(t1)
        threads.append(t2)
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
