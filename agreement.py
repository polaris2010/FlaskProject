from flask import Flask, request, send_file, jsonify
import os
import agreement  # Импортируем модуль agreement

app = Flask(__name__)

# Убедитесь, что директория для договоров существует
if not os.path.exists('./agreements'):
    os.makedirs('./agreements')

@app.route('/create_agreement', methods=['POST'])
def create_agreement_route():
    # Получаем данные из POST-запроса
    data = request.json
    fio = data.get('fio')
    birth_date = data.get('birth_date')
    passport = data.get('passport')
    brand = data.get('brand')
    model = data.get('model')
    year = data.get('year')
    credit_sum = data.get('credit_sum')
    interest_rate = data.get('interest_rate')
    term = data.get('term')
    return_amount = data.get('return_amount')

    # Создаем договор
    file_name = agreement.create_agreement(fio, birth_date, passport, brand, model, year, credit_sum, interest_rate, term, return_amount)

    # Полный путь к файлу
    file_path = os.path.join('./agreements', file_name)

    try:
        # Возвращаем файл для загрузки
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
