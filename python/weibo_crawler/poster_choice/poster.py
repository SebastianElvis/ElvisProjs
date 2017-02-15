class Poster:
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
        self.type = None
        self.follower_num = None
        self.description = None
        self.auth = None
        self.fans_url = None

    def __repr__(self):
        return str(self.__dict__)

