class TS(object):
    def __init__(self):
        print 'init'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(TS, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


if __name__ == '__main__':
    a = TS()
    b = TS()
    print id(a), '---', id(b)