import sqlite3

# Соединяемся с базой данных
def get_connection():
    return sqlite3.connect('borrowers.db')

# Проверяем наличие должника в базе
def check_debtors(fio=None, birth_date=None, passport=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Создаем таблицу при инициализации приложения
        cursor.execute('''CREATE TABLE IF NOT EXISTS debtors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            passport TEXT NOT NULL,
            brand TEXT,
            model TEXT,
            year INTEGER,
            credit_sum INTEGER,
            interest_rate INTEGER,
            time_credit INTEGER,
            return_amount REAL,
            date_over TEXT)''')

        # Формируем запрос с динамическими параметрами
        query = "SELECT * FROM debtors WHERE 1=1"
        params = []

        if fio:
            query += " AND fio = ?"
            params.append(fio)
        if birth_date:
            query += " AND birth_date = ?"
            params.append(birth_date)
        if passport:
            query += " AND passport = ?"
            params.append(passport)

        # Выполняем запрос
        cursor.execute(query, params)
        result = cursor.fetchone()

    return result

# Добавляем заемщика в базу данных и информацию о кредите
def add_debtor(fio, birth_date, passport, brand, model, year, credit_sum, interest_rate, time_credit, return_amount, date_over):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Вставляем данные о заемщике и кредите
        cursor.execute('''INSERT INTO debtors (fio, birth_date, passport, brand, model, year, credit_sum, interest_rate, time_credit, return_amount, date_over)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (fio, birth_date, passport, brand, model, year, credit_sum, interest_rate, time_credit, return_amount, date_over))

        # Сохраняем изменения в базе данных
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Закрываем соединение с базой данных
        conn.close()

