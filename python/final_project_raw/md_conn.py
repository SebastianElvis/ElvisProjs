import pymongo

class md_conn:
    conn = None
    db = None
    col = None
    
    def __init__(self, host, port):
        self.conn = pymongo.MongoClient(host, port)
        
    def select_db(self, db_name):
        self.db = self.conn.get_database(db_name)
        
    def select_collection(self, col_name):
        self.col = self.db.get_collection(col_name)
    
    