

class EtcdError(Exception):

    def __init__(self, error):

        Exception.__init__(self)
        self.error = error


if __name__ == '__main__':

    try:

        raise EtcdError("Connect fail")

    except EtcdError as e:

        raise