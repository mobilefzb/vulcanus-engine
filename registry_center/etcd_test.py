import etcd3

etcd = etcd3.client()
etcd.put("foo", "bar")

value =  etcd.get("foo")
