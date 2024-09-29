from flask import Flask, render_template, request, jsonify
import db
import parse
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Проверяем должника
@app.route('/check_debtor', methods=['POST'])
def check_debtor():
    data = request.json
    fio = data.get('fio')
    birth_date = data.get('birth_date')
    passport = data.get('passport')

    # Проверка наличия необходимых данных
    if not passport and not fio and not birth_date:
        return jsonify({"error": "Данные не указаны"}), 400

    # Проверяем должника в базе данных
    result = db.check_debtors(fio=fio, birth_date=birth_date, passport_data=passport)

    if result:
        return jsonify({"status": "found", "message": "Должник найден!"})
    else:
        return jsonify({"status": "not_found", "message": "Должник не найден."})


# Расчет средней цены авто
@app.route('/calculatePrice', methods=['POST'])
def calculate_price():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')

    if not brand or not model or not year:
        return jsonify({"error": "Не указаны все данные для расчета"}), 400

    # Ищем среднюю цену авто
    url = parse.get_avito_url(brand, model, year)
    if not url:
        return jsonify({"error": "Не удалось найти URL для указанных данных"}), 400

    avg_price = parse.scrape_item_prices(url)

    if avg_price > 0:
        return jsonify({"status": "success", "avg_price": avg_price})
    else:
        return jsonify({"status": "error", "message": "Не удалось рассчитать стоимость авто"}), 500


@app.route('/calculate', methods=['POST'])
def calculate():
    credit_sum = float(request.form['credit_sum'])  # Уже рассчитывается в форме
    interest_rate = float(request.form['interest_rate'])
    time_credit = int(request.form['time_credit'])

    # Логика расчета общей суммы к возврату
    total_payment = credit_sum + (credit_sum * (interest_rate / 100) * time_credit)

    # Расчет даты возврата
    return_date = datetime.now() + timedelta(days=time_credit * 30)  # Предполагаем, что срок в месяцах

    # Возвращаем результат в формате JSON
    return jsonify({
        'total_payment': round(total_payment, 2),
        'return_date': return_date.strftime('%Y-%m-%d')
    })


# @app.route('/credit', methods=['POST'])
# def credit():
    # - кнопка "оформить кредит" должна добавлять данные заемщика, авто и кредита в таблицу debtors БД borrowers.db;
    # - создать файл c именем заемщика fio в формате txt по образцу agreement.py;
    # - после выдать сообщение "заемщеик внесен в базу данных, договор займа сформирован".


if __name__ == '__main__':
    app.run(debug=True)
