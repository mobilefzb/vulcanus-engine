import threading
from etcd3gw.client import Etcd3Client

threads = []
etcd = Etcd3Client("localhost", 2379)

def watch_etcd_event(key):

        events_iterator, cancel = etcd.watch_prefix(key)

        for event in events_iterator:
            print event['kv']['key']
            print event['kv']['value']


t1 = threading.Thread(target=watch_etcd_event, args=('foo',))
threads.append(t1)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

    print "all over"