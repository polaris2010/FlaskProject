import logging
from flask import Flask, render_template, request, jsonify
import db
import parse
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(filename='app.txt', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Логируем запуск приложения
logging.info('Приложение запущено')

@app.route('/')
def index():
    app.logger.info('Отображение главной страницы')
    return render_template('index.html')

# Проверяем должника
@app.route('/check_debtor', methods=['POST'])
def check_debtor():
    data = request.json
    fio = data.get('fio')
    birth_date = data.get('birth_date')
    passport = data.get('passport')

    app.logger.info(f'Проверка должника: ФИО={fio}, Дата рождения={birth_date}, Паспорт={passport}')

    # Проверка наличия необходимых данных
    if not passport and not fio and not birth_date:
        app.logger.warning('Не указаны необходимые данные для проверки должника')
        return jsonify({"error": "Данные не указаны"}), 400

    # Проверяем должника в базе данных
    result = db.check_debtors(fio=fio, birth_date=birth_date, passport=passport)

    if result:
        app.logger.info('Должник найден')
        return jsonify({"status": "found", "message": "Кредит выдать нельзя"})
    else:
        app.logger.info('Должник не найден')
        return jsonify({"status": "not_found", "message": "Кредит возможен"})

# Расчет средней цены авто
@app.route('/calculatePrice', methods=['POST'])
def calculate_price():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')

    app.logger.info(f'Запрос на расчет средней цены авто: Марка={brand}, Модель={model}, Год={year}')

    if not brand or not model or not year:
        app.logger.warning('Не указаны все данные для расчета средней цены авто')
        return jsonify({"error": "Не указаны все данные для расчета"}), 400

    # Ищем среднюю цену авто
    url = parse.get_avito_url(brand, model, year)
    if not url:
        app.logger.error('Не удалось найти URL для указанных данных')
        return jsonify({"error": "Не удалось найти URL для указанных данных"}), 400

    avg_price = parse.scrape_item_prices(url)

    if avg_price > 0:
        app.logger.info(f'Средняя цена авто: {avg_price}')
        return jsonify({"status": "success", "avg_price": avg_price})
    else:
        app.logger.error('Не удалось рассчитать стоимость авто')
        return jsonify({"status": "error", "message": "Не удалось рассчитать стоимость авто"}), 500

# Расчет кредита
@app.route('/calculate', methods=['POST'])
def calculate():
    credit_sum = float(request.form['credit_sum'])
    interest_rate = float(request.form['interest_rate'])
    time_credit = int(request.form['time_credit'])

    app.logger.info(f'Расчет кредита: Сумма={credit_sum}, Процентная ставка={interest_rate}, Срок={time_credit} месяцев')

    total_payment = credit_sum + (credit_sum * (interest_rate / 100) * time_credit)
    return_date = datetime.now() + timedelta(days=time_credit * 30)

    app.logger.info(f'Общая сумма к возврату: {total_payment}, Дата возврата: {return_date.strftime("%Y-%m-%d")}')

    return jsonify({
        'total_payment': round(total_payment, 2),
        'return_date': return_date.strftime('%Y-%m-%d')
    })

# Новый маршрут для оформления кредита
@app.route('/credit', methods=['POST'])
def credit():
    try:
        # Получаем данные из JSON-запроса
        data = request.json

        # Получаем значения
        fio = data.get('fio')
        passport = data.get('passport')
        birth_date = data.get('birth_date')
        credit_sum = data.get('credit_sum')
        interest_rate = data.get('interest_rate')
        time_credit = data.get('time_credit')
        car_brand = data.get('car_brand')
        car_model = data.get('car_model')
        car_year = data.get('car_year')

        # Проверка обязательных полей
        missing_fields = []
        if not fio: missing_fields.append('fio')
        if not passport: missing_fields.append('passport')
        if not birth_date: missing_fields.append('birth_date')
        if not credit_sum: missing_fields.append('credit_sum')
        if not interest_rate: missing_fields.append('interest_rate')
        if not time_credit: missing_fields.append('time_credit')
        if not car_brand: missing_fields.append('car_brand')
        if not car_model: missing_fields.append('car_model')
        if not car_year: missing_fields.append('car_year')

        if missing_fields:
            app.logger.warning(f'Отсутствуют обязательные поля: {", ".join(missing_fields)}')
            return jsonify({
                'status': 'error',
                'message': f'Не все обязательные поля присутствуют: {", ".join(missing_fields)}'
            }), 400

        # Преобразование в числовые значения, если все поля присутствуют
        credit_sum = float(credit_sum)
        interest_rate = float(interest_rate)
        time_credit = int(time_credit)
        car_year = int(car_year)

        app.logger.info(f'Оформление кредита для {fio} на автомобиль {car_brand} {car_model} {car_year}')

        # Возвращаем сумму кредита и дату возврата
        return_amount = credit_sum + (credit_sum * (interest_rate / 100) * time_credit)
        return_date = datetime.now() + timedelta(days=time_credit * 30)
        date_over = return_date.strftime('%Y-%m-%d')

        # Добавление данных заемщика в базу данных
        db.add_debtor(fio, birth_date, passport, car_brand, car_model, car_year, credit_sum, interest_rate, time_credit, return_amount, date_over)

        # Создание соглашения для заемщика
        agreement_text = f"""Договор займа
Заемщик: {fio}
Паспорт: {passport}
Дата рождения: {birth_date}
Кредит: {credit_sum} руб. под {interest_rate}% на {time_credit} месяцев
Автомобиль: {car_brand} {car_model} {car_year}
Дата: {datetime.now().strftime('%Y-%m-%d')}
        """

        filename = f"{fio.replace(' ', '_')}_agreement.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(agreement_text)

        app.logger.info(f'Договор займа для {fio} сохранен в файл {filename}')

        return jsonify({
            'status': 'success',
            'message': 'Заемщик внесен в базу данных, договор займа сформирован',
            'agreement_file': filename
        })

    except Exception as e:
        app.logger.error(f'Ошибка при оформлении кредита: {e}')
        return jsonify({
            'status': 'error',
            'message': 'Произошла ошибка при оформлении кредита'
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
