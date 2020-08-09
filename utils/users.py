from utils.db_helper import DatabaseHelper

import config

def create_user_db():
    db = DatabaseHelper(config.get('USERS_DB', 'users.db'))

    db.conn.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            user_id             TEXT,
            guild_id            TEXT,
            active              INTEGER,
            PRIMARY KEY (user_id, guild_id)
        )
    ''')
    db.conn.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS ix_user_handle_guild_handle
        ON user_handle (guild_id, handle)
    ''')
