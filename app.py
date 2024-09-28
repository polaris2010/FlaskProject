from flask import Flask, render_template, request, jsonify
import db  # Импортируем ваш модуль для работы с базой данных
import parse  # Импортируем ваш модуль для парсинга цен
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Маршрут для проверки должника
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


# Маршрут для расчета средней цены авто
@app.route('/calculatePrice', methods=['POST'])
def calculate_price():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')

    if not brand or not model or not year:
        return jsonify({"error": "Не указаны все данные для расчета"}), 400

    # Парсим среднюю цену авто
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
    credit_sum = float(request.form['credit_sum'])
    percent = float(request.form['percent'])
    time_credit = int(request.form['time_credit'])

    # Рассчитываем общую сумму к возврату
    total_payment = credit_sum + (credit_sum * (percent / 100) * time_credit)

    # Рассчитываем дату возврата
    return_date = datetime.now() + timedelta(days=time_credit * 30)  # Предполагаем, что срок в месяцах

    # Форматируем дату для отображения
    return_date_str = return_date.strftime('%Y-%m-%d')

    return jsonify({
        'total_payment': round(total_payment, 2),
        'return_date': return_date_str
    })


if __name__ == '__main__':
    app.run(debug=True)
