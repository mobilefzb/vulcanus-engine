from etcd3gw.client import Etcd3Client

client = Etcd3Client()
msg =  client.get_prefix("/")
print msg