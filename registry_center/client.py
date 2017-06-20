from etcd3gw.client import Etcd3Client


class Register(object):

    def __init__(self, req_host, req_port):

        self.__client = Etcd3Client(host=req_host, port=req_port)

    def get_client(self):

        return self.__client

    def put_value(self, key, value):

        """
        :param key:
        :param value:
        :return:    put success return True, faild False
        """

        return self.__client.put(key,value)

    def get_value(self, key):


        """

        :param key:
        :return:  return a list
        """

        return self.__client.get(key)

    def delete_vaule(self, key):

        """

        :param key:
        :return: delete success return True, faild False
        """

        return self.__client.delete(key)

    def get_value_by_prefix(self, prefix):

        self.__client.get_prefix(prefix)

    def watch_value(self, key):

        events_iterator, cancel = self.__client.watch(key)
        for event in events_iterator:
            print event['kv']['key']
            print event['kv']['value']

    def watch_value_by_perfix(self, perfix):

        events_iterator, cancel = self.__client.watch_prefix(perfix)
        for event in events_iterator:
            print event['kv']['key']
            print event['kv']['value']

if __name__ == '__main__':

    client = Etcd3Client()
    print client.get_all()