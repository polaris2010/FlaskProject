from flask import Flask, render_template, request, jsonify
import db
import parse
import agreement

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Валидация паспортных данных
def validate_passport(passport):
    import re
    if re.match(r'^\d{2} \d{2} \d{6}$', passport):
        return True
    return False

# Проверка должника
@app.route('/check_debtor', methods=['POST'])
def check_debtor():
    fio = request.form['fio']
    birth_date = request.form['birth_date']
    passport = request.form['passport']

    if not validate_passport(passport):
        return jsonify({"error": "Некорректные паспортные данные"}), 400

    search = db.check_debtors(fio=fio, birth_date=birth_date, passport_data=passport)

    if search:
        return jsonify({"message": "Запись найдена, кредит невозможен", "status": "error"})
    else:
        return jsonify({"message": "Запись не найдена", "status": "success"})

# Расчет суммы кредита
@app.route('/calculate_loan', methods=['POST'])
def calculate_loan():
    try:
        loan_amount = float(request.form['loan_amount'])
        interest_rate = float(request.form['interest_rate']) / 100
        term_months = int(request.form['term_months'])

        return_amount = loan_amount * (1 + interest_rate * term_months)
        return jsonify({"return_amount": round(return_amount, 2)})
    except ValueError:
        return jsonify({"error": "Некорректные данные"}), 400

# Оформление кредита
@app.route('/submit_loan', methods=['POST'])
def submit_loan():
    try:
        fio = request.form['fio']
        birth_date = request.form['birth_date']
        passport = request.form['passport']
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        loan_amount = float(request.form['loan_amount'])
        return_amount = float(request.form['return_amount'])

        # Сохранение данных в базу
        db.save_loan(fio=fio, birth_date=birth_date, passport_data=passport,
                     brand=brand, model=model, year=year, loan_amount=loan_amount, return_amount=return_amount)

        # Создание договора
        agreement_file = agreement.create_agreement(fio=fio, birth_date=birth_date, passport=passport,
                                                    brand=brand, model=model, year=year,
                                                    credit_sum=loan_amount, return_amount=return_amount)

        return jsonify({"message": f"Кредит оформлен! Договор сохранен: {agreement_file}", "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
