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
        for ds in r:
            ds['_id'] = str(ds['_id'])
        return r

    def get_all_processed_companies(self):
        companies = self.find_all('company')
        for company in companies:
            company['_id'] = str(company['_id'])
        return companies

    def get_records(self, page=1, num=10, type='all', sort=1):
        condition_dict = {}

        data_sources = self.get_all_data_sources()
        if type != 'all':
            for single_ds in data_sources:
                if single_ds['type'] != type:
                    data_sources.remove(single_ds)
        filtered_data_source_dict = {}
        for single_ds in data_sources:
            filtered_data_source_dict[single_ds['_id']] = single_ds
        '''
        if type != 'all':
            condition_dict['type'] = type
        '''
        record_col = self.get_col('record')
        if num == -1:
            records_cursor = record_col.find().sort('time', sort)
        else:
            records_cursor = record_col.find().sort('time', sort).limit(num).skip((page-1)*num)
        records_list = []
        for s in records_cursor:
            s['_id'] = str(s['_id'])
            if s['poster_id'] in filtered_data_source_dict:
                s['poster'] = filtered_data_source_dict[s['poster_id']]['name']
                s['type'] = filtered_data_source_dict[s['poster_id']]['type']
            else:
                continue
            records_list.append(s)
        result = dict()
        result['records_list'] = records_list
        result['count'] = record_col.count()
        return result


dao = BaseDAO()

if __name__ == '__main__':
    dao = BaseDAO()
    r = dao.get_records(type='all', num=-1)
    print r['count']
    r = dao.get_records(type='financial_news', num=-1)
    print r['count']
