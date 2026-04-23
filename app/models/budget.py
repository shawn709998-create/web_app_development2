from app.models.database import get_db_connection

class BudgetModel:
    @staticmethod
    def create(month, amount, category_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO budget (month, amount, category_id) VALUES (?, ?, ?)',
            (month, amount, category_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        budgets = conn.execute('SELECT * FROM budget ORDER BY month DESC').fetchall()
        conn.close()
        return [dict(row) for row in budgets]

    @staticmethod
    def get_by_id(budget_id):
        conn = get_db_connection()
        budget = conn.execute('SELECT * FROM budget WHERE id = ?', (budget_id,)).fetchone()
        conn.close()
        return dict(budget) if budget else None

    @staticmethod
    def get_by_month(month):
        conn = get_db_connection()
        budgets = conn.execute('SELECT * FROM budget WHERE month = ?', (month,)).fetchall()
        conn.close()
        return [dict(row) for row in budgets]

    @staticmethod
    def update(budget_id, amount):
        conn = get_db_connection()
        conn.execute(
            'UPDATE budget SET amount = ? WHERE id = ?',
            (amount, budget_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(budget_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM budget WHERE id = ?', (budget_id,))
        conn.commit()
        conn.close()
