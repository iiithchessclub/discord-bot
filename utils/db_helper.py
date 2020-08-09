import sqlite3

import config

class DatabaseHelper:
    def __init__(self, db_file=None):
        self.db_file = db_file or config.get('DEFAULT_DB', 'default.db')
        self.db_path = config.get('APP_DATA_DIR', 'data/') + self.db_file
        self.conn = sqlite3.connect(self.db_path)
    
    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.commit()
        self.conn.close()
