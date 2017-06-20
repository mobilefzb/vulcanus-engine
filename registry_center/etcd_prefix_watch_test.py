from etcd3gw.client import Etcd3Client

def watch_etcd_event(key):
    client = Etcd3Client()
    events_iterator, cancel = client.watch_prefix("/registry/service")
    for event in events_iterator:
        print event['kv']['key']
        print event['kv']['value']


import threading
threads = []
t1 = threading.Thread(target=watch_etcd_event, args=('foo',))
threads.append(t1)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
