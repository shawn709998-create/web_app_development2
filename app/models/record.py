from app.models.database import get_db_connection
import logging

class RecordModel:
    @staticmethod
    def create(amount, type, date, note, category_id):
        """
        新增一筆收支紀錄。
        :param amount: 金額 (float)
        :param type: 收支屬性 ('income' 或 'expense')
        :param date: 發生日期 (YYYY-MM-DD)
        :param note: 備註 (str)
        :param category_id: 分類 ID (int)
        :return: 新增的紀錄 ID，失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO record (amount, type, date, note, category_id) VALUES (?, ?, ?, ?, ?)',
                (amount, type, date, note, category_id)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            logging.error(f"新增收支紀錄失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有歷史收支紀錄，並加入分類名稱。
        :return: 包含字典的 list
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT record.*, category.name as category_name 
                FROM record 
                LEFT JOIN category ON record.category_id = category.id
                ORDER BY record.date DESC, record.created_at DESC
            '''
            records = conn.execute(query).fetchall()
            return [dict(row) for row in records]
        except Exception as e:
            logging.error(f"取得所有收支紀錄失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        取得單筆收支紀錄。
        :param record_id: 紀錄 ID
        :return: 紀錄資料的字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            record = conn.execute('SELECT * FROM record WHERE id = ?', (record_id,)).fetchone()
            return dict(record) if record else None
        except Exception as e:
            logging.error(f"取得單筆收支紀錄失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(record_id, amount, type, date, note, category_id):
        """
        更新單筆收支紀錄。
        :param record_id: 紀錄 ID
        :param amount: 新金額
        :param type: 新屬性
        :param date: 新日期
        :param note: 新備註
        :param category_id: 新分類 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE record SET amount = ?, type = ?, date = ?, note = ?, category_id = ? WHERE id = ?',
                (amount, type, date, note, category_id, record_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"更新收支紀錄失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(record_id):
        """
        刪除單筆收支紀錄。
        :param record_id: 紀錄 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM record WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"刪除收支紀錄失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
