import logging
from flask import Flask, render_template, request, jsonify
import db
import parse
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Логируем запуск приложения
app.logger.info('Приложение запущено')


@app.route('/')
def index():
    app.logger.info('Отображение главной страницы')
    return render_template('index.html')


@app.route('/check_debtor', methods=['POST'])
def check_debtor():
    data = request.json
    fio = data.get('fio')
    birth_date = data.get('birth_date')
    passport = data.get('passport')

    app.logger.info(f'Проверка должника: ФИО={fio}, Дата рождения={birth_date}, Паспорт={passport}')

    if not any([passport, fio, birth_date]):
        app.logger.warning('Не указаны необходимые данные для проверки должника')
        return jsonify({"error": "Данные не указаны"}), 400

    result = db.check_debtors(fio=fio, birth_date=birth_date, passport=passport)

    if result:
        app.logger.info('Должник найден')
        return jsonify({"status": "found", "message": "Кредит выдать нельзя"})
    else:
        app.logger.info('Должник не найден')
        return jsonify({"status": "not_found", "message": "Кредит возможен"})


@app.route('/calculatePrice', methods=['POST'])
def calculate_price():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')

    app.logger.info(f'Запрос на расчет средней цены авто: Марка={brand}, Модель={model}, Год={year}')

    if not all([brand, model, year]):
        app.logger.warning('Не указаны все данные для расчета средней цены авто')
        return jsonify({"error": "Не указаны все данные для расчета"}), 400

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


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        credit_sum = float(request.form['credit_sum'])
        interest_rate = float(request.form['interest_rate'])
        time_credit = int(request.form['time_credit'])

        app.logger.info(
            f'Расчет кредита: Сумма={credit_sum}, Процентная ставка={interest_rate}, Срок={time_credit} месяцев')

        total_payment = credit_sum * (1 + (interest_rate / 100) * (time_credit / 1))
        return_date = datetime.now() + timedelta(days=time_credit * 30)

        app.logger.info(f'Общая сумма к возврату: {total_payment}, Дата возврата: {return_date.strftime("%Y-%m-%d")}')

        return jsonify({
            'total_payment': round(total_payment, 2),
            'return_date': return_date.strftime('%Y-%m-%d')
        })
    except ValueError as e:
        app.logger.error(f'Ошибка при расчете кредита: {e}')
        return jsonify({"error": "Неверный формат данных"}), 400


@app.route('/credit', methods=['POST'])
def credit():
    try:
        app.logger.info("Начало выполнения функции credit()")
        data = request.json
        app.logger.info(f"Полученные данные: {data}")

        credit_sum = float(data['credit_sum'])
        interest_rate = float(data['interest_rate'])
        time_credit = int(data['time_credit'])
        car_year = int(data['car_year'])

        app.logger.info(f'Оформление кредита для {data["fio"]} на автомобиль {data["car_brand"]} {data["car_model"]} {car_year}')

        # Расчет общей суммы кредита с учетом ежемесячного начисления процентов
        monthly_rate = interest_rate / 100 / 1
        total_payment = credit_sum * (monthly_rate * (1 + monthly_rate)**time_credit) / ((1 + monthly_rate)**time_credit - 1) * time_credit
        return_date = datetime.now() + timedelta(days=time_credit * 30)
        date_over = return_date.strftime('%Y-%m-%d')

        app.logger.info("Попытка добавления записи в базу данных")
        # Запись информации о кредите в базу данных
        db.add_debtor(
            fio=data['fio'],
            birth_date=data['birth_date'],
            passport=data['passport'],
            brand=data['car_brand'],
            model=data['car_model'],
            year=car_year,
            credit_sum=credit_sum,
            interest_rate=interest_rate,
            time_credit=time_credit,
            return_amount=total_payment,
            date_over=date_over
        )

        app.logger.info(f'Информация о кредите для {data["fio"]} успешно записана в базу данных')

        agreement_text = f"""Договор займа
Заемщик: {data['fio']}
Паспорт: {data['passport']}
Дата рождения: {data['birth_date']}
Кредит: {credit_sum} руб. под {interest_rate}% на {time_credit} месяцев
Автомобиль: {data['car_brand']} {data['car_model']} {car_year}
Общая сумма к возврату: {total_payment:.2f} руб.
Дата возврата: {date_over}
Дата оформления: {datetime.now().strftime('%Y-%m-%d')}
        """

        filename = f"{data['fio'].replace(' ', '_')}_agreement.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(agreement_text)

        app.logger.info(f'Договор займа для {data["fio"]} сохранен в файл {filename}')

        return jsonify({
            'status': 'success',
            'message': 'Кредит оформлен, договор сформирован!'
        })

    except Exception as e:
        app.logger.error(f'Ошибка при оформлении кредита: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Произошла ошибка при оформлении кредита: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True)