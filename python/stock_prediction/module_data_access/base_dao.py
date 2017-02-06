import pymongo


class BaseDAO:
    def __init__(self, db='weibo'):
        self.client = pymongo.MongoClient()
        self.db_name = db

    def get_client(self):
        return self.client

    def get_col(self, col):
        return self.client.get_database(self.db_name).get_collection(col)

    def find_all(self, col):
        cursor = self.get_col(col).find()
        result = []
        for i in range(cursor.count()):
            result.append(cursor.next())
        return result  # list[dict]

    def get_all_data_sources(self):
        r = self.find_all('data_source')
        l = [ds['url'] for ds in r]
        return l

    def get_all_processed_companies(self):
        companies = self.find_all('company')
        for company in companies:
            company['_id'] = str(company['_id'])
        return companies

    def get_records(self, page=1, num=10, type='all', sort=1):
        condition_dict = {}
        if type is not 'all':
            condition_dict['type'] = type
        record_col = self.get_col('record')
        records_cursor = record_col.find(condition_dict).sort('time', sort).limit(num).skip((page-1)*num)
        records_list = []
        for s in records_cursor:
            s['_id'] = str(s['_id'])
            records_list.append(s)
        return records_list


dao = BaseDAO()

if __name__ == '__main__':
    dao = BaseDAO()
    r = dao.find_all('company')
    print r
