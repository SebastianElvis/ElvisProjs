import pymongo


class BaseDAO:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_name = 'weibo'

    def get_client(self):
        return self.client

    def get_col(self, col):
        return self.client.get_database(self.db_name).get_collection(col)

    def find_all(self, col):
        cursor = self.get_col(col).find()
        result = []
        for i in range(cursor.count()):
            result.append(cursor.next())
        return result # list[dict]

if __name__ == '__main__':
    dao = BaseDAO()
    r =  dao.find_all('company')
    print r