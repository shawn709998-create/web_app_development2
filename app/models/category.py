from app.models.database import get_db_connection

class CategoryModel:
    @staticmethod
    def create(name, type, is_default=False):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO category (name, type, is_default) VALUES (?, ?, ?)',
            (name, type, is_default)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM category').fetchall()
        conn.close()
        return [dict(row) for row in categories]

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        category = conn.execute('SELECT * FROM category WHERE id = ?', (category_id,)).fetchone()
        conn.close()
        return dict(category) if category else None

    @staticmethod
    def update(category_id, name, type):
        conn = get_db_connection()
        conn.execute(
            'UPDATE category SET name = ?, type = ? WHERE id = ? AND is_default = 0',
            (name, type, category_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(category_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM category WHERE id = ? AND is_default = 0', (category_id,))
        conn.commit()
        conn.close()
