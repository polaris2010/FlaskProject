import sqlite3  # Импортируем библиотеку для работы с SQLite

def get_connection():
    """Функция для получения соединения с базой данных."""
    return sqlite3.connect('your_database.db')  # Замените 'your_database.db' на имя вашей базы данных

def check_debtors(fio=None, birth_date=None, passport_data=None):
    """Проверка должников по ФИО, дате рождения и паспортным данным."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Создаем таблицу только при инициализации приложения
        cursor.execute('''CREATE TABLE IF NOT EXISTS debtors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            passport_data TEXT NOT NULL,
            brand TEXT,
            model TEXT,
            year INTEGER,
            loan_amount REAL,
            return_amount REAL
        )''')

        # Формируем запрос с динамическими параметрами
        query = "SELECT * FROM debtors WHERE 1=1"
        params = []

        if fio:
            query += " AND fio = ?"
            params.append(fio)
        if birth_date:
            query += " AND birth_date = ?"
            params.append(birth_date)
        if passport_data:
            query += " AND passport_data = ?"
            params.append(passport_data)

        # Выполняем запрос
        cursor.execute(query, params)
        result = cursor.fetchone()

    return result
