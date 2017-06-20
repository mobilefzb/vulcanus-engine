

class FormatError(Exception):

    def __init__(self, err):

        Exception.__init__(self)

        self.err = err


if __name__ == '__main__':

    try:

        raise FormatError("prase fail")

    except FormatError as e:

        raise