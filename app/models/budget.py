from app.models.database import get_db_connection
import logging

class BudgetModel:
    @staticmethod
    def create(month, amount, category_id=None):
        """
        新增預算設定。
        :param month: 月份 (YYYY-MM)
        :param amount: 預算金額 (float)
        :param category_id: 分類 ID，可選 (int)
        :return: 新增的紀錄 ID，失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO budget (month, amount, category_id) VALUES (?, ?, ?)',
                (month, amount, category_id)
            )
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Exception as e:
            logging.error(f"新增預算失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有預算設定。
        :return: 包含字典的 list
        """
        try:
            conn = get_db_connection()
            budgets = conn.execute('SELECT * FROM budget ORDER BY month DESC').fetchall()
            return [dict(row) for row in budgets]
        except Exception as e:
            logging.error(f"取得所有預算失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(budget_id):
        """
        取得單筆預算設定。
        :param budget_id: 預算 ID
        :return: 預算資料字典，不存在則回傳 None
        """
        try:
            conn = get_db_connection()
            budget = conn.execute('SELECT * FROM budget WHERE id = ?', (budget_id,)).fetchone()
            return dict(budget) if budget else None
        except Exception as e:
            logging.error(f"取得單筆預算失敗: {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_month(month):
        """
        取得特定月份的所有預算設定。
        :param month: 月份 (YYYY-MM)
        :return: 包含字典的 list
        """
        try:
            conn = get_db_connection()
            budgets = conn.execute('SELECT * FROM budget WHERE month = ?', (month,)).fetchall()
            return [dict(row) for row in budgets]
        except Exception as e:
            logging.error(f"取得特定月份預算失敗: {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(budget_id, amount):
        """
        更新預算金額。
        :param budget_id: 預算 ID
        :param amount: 新預算金額
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE budget SET amount = ? WHERE id = ?',
                (amount, budget_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"更新預算失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(budget_id):
        """
        刪除單筆預算設定。
        :param budget_id: 預算 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM budget WHERE id = ?', (budget_id,))
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"刪除預算失敗: {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
