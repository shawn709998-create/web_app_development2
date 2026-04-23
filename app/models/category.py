from app.models.database import get_db_connection
import logging

class CategoryModel:
    @staticmethod
    def create(name, type, is_default=False):
        """
        新增一筆分類。
        :param name: 分類名稱 (str)
        :param type: 分類屬性 ('income' 或 'expense')
        :param is_default: 是否為內建分類 (bool)
        :return: 新增的紀錄 ID，失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO category (name, type, is_default) VALUES (?, ?, ?)',
                (name, type, is_default)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            logging.error(f"新增分類失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有分類。
        :return: 包含字典的 list
        """
        try:
            conn = get_db_connection()
            categories = conn.execute('SELECT * FROM category').fetchall()
            return [dict(row) for row in categories]
        except Exception as e:
            logging.error(f"取得所有分類失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(category_id):
        """
        取得單筆分類。
        :param category_id: 分類 ID
        :return: 分類資料的字典，若不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            category = conn.execute('SELECT * FROM category WHERE id = ?', (category_id,)).fetchone()
            return dict(category) if category else None
        except Exception as e:
            logging.error(f"取得分類失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(category_id, name, type):
        """
        更新指定的自訂分類 (內建分類不可更新)。
        :param category_id: 分類 ID
        :param name: 新分類名稱
        :param type: 新分類屬性
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE category SET name = ?, type = ? WHERE id = ? AND is_default = 0',
                (name, type, category_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"更新分類失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(category_id):
        """
        刪除指定的自訂分類 (內建分類不可刪除)。
        :param category_id: 分類 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM category WHERE id = ? AND is_default = 0', (category_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"刪除分類失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
