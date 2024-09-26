import sqlite3

DATABASE = 'borrowers.db'

def get_connection():
    """Функция для получения подключения к базе данных."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Это позволяет получать результаты как словари
    return conn

def check_debtors(fio=None, birth_date=None, passport_data=None):
    """Проверка должников по ФИО, дате рождения и паспортным данным."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Создаем таблицу, если она не существует
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS debtors (
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

def save_loan(fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount):
    """Сохранение данных по кредиту."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Вставляем данные в таблицу
            cursor.execute('''
            INSERT INTO debtors (fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (fio, birth_date, passport_data, brand, model, year, loan_amount, return_amount))

            # Сохраняем изменения
            conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False  # Можно вернуть False или сообщение об ошибке для дальнейшей обработки

    return True  # Успешное завершение операции
