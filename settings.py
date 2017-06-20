import ConfigParser
import os
import sys

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(sys.path[0], "config/vulcanus.conf"))

ETCD_HOST = cf.get("etcd", "host")
ETCD_PORT = cf.get("etcd", "port")