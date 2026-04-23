from app.models.database import get_db_connection

class RecordModel:
    @staticmethod
    def create(amount, type, date, note, category_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO record (amount, type, date, note, category_id) VALUES (?, ?, ?, ?, ?)',
            (amount, type, date, note, category_id)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        query = '''
            SELECT record.*, category.name as category_name 
            FROM record 
            LEFT JOIN category ON record.category_id = category.id
            ORDER BY record.date DESC, record.created_at DESC
        '''
        records = conn.execute(query).fetchall()
        conn.close()
        return [dict(row) for row in records]

    @staticmethod
    def get_by_id(record_id):
        conn = get_db_connection()
        record = conn.execute('SELECT * FROM record WHERE id = ?', (record_id,)).fetchone()
        conn.close()
        return dict(record) if record else None

    @staticmethod
    def update(record_id, amount, type, date, note, category_id):
        conn = get_db_connection()
        conn.execute(
            'UPDATE record SET amount = ?, type = ?, date = ?, note = ?, category_id = ? WHERE id = ?',
            (amount, type, date, note, category_id, record_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(record_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM record WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
