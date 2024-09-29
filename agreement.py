import datetime

def create_agreement(fio, birth_date, passport, brand, model, year, credit_sum, interest_rate, time_credit, return_amount, date_over):
    # Получаем текущую дату
    today_date = datetime.datetime.now().strftime("%d.%m.%Y")

    # Формируем содержание договора
    agreement_text = f"""
    ДОГОВОР ЗАЙМА
    
    Москва, {today_date}
    
    Автоломбард, далее «Кредитор», с одной стороны и {fio}, далее «Заемщик», с другой стороны, 
    заключили настоящий договор о нижеследующем:
    
    По настоящему договору Автоломбард передает в собственность Заемщика денежные средства в сумме {credit_sum} 
    под {interest_rate} % в месяц, на срок {time_credit} месяцев, под залог автомобиля {brand} {model} {year},
    а Заемщик обязуется возвратить Кредитору {return_amount} в срок до {date_over}.

    Стороны:
    
    Автоломбард: ИНН 00000000000, Адрес: Москва, Кремль
    Заемщик: {fio}, дата рождения {birth_date}, паспорт {passport}

    Подписи сторон:
    __________________________________
    """

    # Генерируем имя файла на основе ФИО и текущей даты
    file_name = f"agreement_{fio.replace(' ', '_')}_{today_date}.txt"

    # Записываем текст договора в файл
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(agreement_text)

    return file_name
