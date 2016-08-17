import pymongo, threading

class md_conn:
    conn = None
    db = None
    col = None
    lock = threading.Lock()
    
    def __init__(self, host='127.0.0.1', port=27017):
        self.conn = pymongo.MongoClient(host, port)
        
    def select_db(self, db_name):
        self.db = self.conn.get_database(db_name)
        
    def select_collection(self, col_name):
        self.col = self.db.get_collection(col_name)
    
    def insert_many_to(self, db_name, col_name, result_list):
        self.lock.acquire()
        self.select_db(db_name)
        self.select_collection(col_name)
        self.col.insert_many(result_list)
        self.lock.release()
    
    def insert_one_to(self, db_name, col_name, single_result):
        self.lock.acquire()
        self.select_db(db_name)
        self.select_collection(col_name)
        self.col.insert_one(single_result)
        self.lock.release()
    