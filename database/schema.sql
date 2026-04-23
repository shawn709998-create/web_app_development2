CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    is_default BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    amount REAL NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

-- 預設內建分類
INSERT INTO category (name, type, is_default) VALUES ('薪水', 'income', 1);
INSERT INTO category (name, type, is_default) VALUES ('投資', 'income', 1);
INSERT INTO category (name, type, is_default) VALUES ('飲食', 'expense', 1);
INSERT INTO category (name, type, is_default) VALUES ('交通', 'expense', 1);
INSERT INTO category (name, type, is_default) VALUES ('娛樂', 'expense', 1);
INSERT INTO category (name, type, is_default) VALUES ('居家', 'expense', 1);
