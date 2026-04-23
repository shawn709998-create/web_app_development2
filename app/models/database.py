import sqlite3
import os
import logging

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    取得與 SQLite 資料庫的連線，並設定 row_factory 讓結果能以字典方式存取。
    回傳 sqlite3.Connection 物件。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logging.error(f"資料庫連線失敗: {e}")
        raise

def init_db():
    """
    初始化資料庫，根據 schema.sql 建立資料表與預設資料。
    """
    try:
        conn = get_db_connection()
        schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        conn.commit()
    except Exception as e:
        logging.error(f"資料庫初始化失敗: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()
