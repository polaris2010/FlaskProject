$(document).ready(function() {
    // Обработчик нажатия кнопки "Проверить должника"
    $('#checkDebtor').on('click', function() {
        var fio = $('#fio').val();
        var birth_date = $('#birth_date').val();
        var passport = $('#passport').val();

        // Проверка обязательных полей перед отправкой запроса
        if (!fio || !birth_date || !passport) {
            $('#resultMessage').text("Пожалуйста, заполните все поля!").css('color', 'red');
            return;
        }

        $.ajax({
            url: '/check_debtor',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                fio: fio,
                birth_date: birth_date,
                passport: passport
            }),
            success: function(response) {
                if (response.status === 'found') {
                    $('#resultMessage').text("Кредит выдать нельзя").css('color', 'red');
                } else {
                    $('#resultMessage').text("Кредит возможен").css('color', 'green');
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                $('#resultMessage').text("Произошла ошибка при проверке должника.").css('color', 'red');
            }
        });
    });

    // Обработка расчета стоимости авто
    $('#calculatePrice').click(function() {
        var brand = $('#brand').val();
        var model = $('#model').val();
        var year = $('#year').val();

        // Проверка обязательных полей
        if (!brand || !model || !year) {
            alert("Пожалуйста, заполните все поля!");
            return;
        }

        $.ajax({
            url: '/calculatePrice',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                brand: brand,
                model: model,
                year: year
            }),
            success: function(response) {
                if (response.status === 'success') {
                    var carPrice = parseFloat(response.avg_price); // Преобразуем в число
                    $('#car_price').val(carPrice.toFixed(2) + ' руб.');

                    // Рассчитываем 60% от стоимости авто
                    var creditSum = carPrice * 0.6;
                    $('#credit_sum').val(creditSum.toFixed(2));
                } else {
                    alert('Ошибка: ' + response.message);
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Произошла ошибка: ' + xhr.responseJSON.error);
            }
        });
    });

    // Автоматический расчет суммы кредита при изменении поля "Стоимость авто"
    $('#car_price').on('input', function() {
        var carPrice = parseFloat($(this).val());
        if (!isNaN(carPrice)) {
            var creditSum = carPrice * 0.6;
            $('#credit_sum').val(creditSum.toFixed(2));
        } else {
            $('#credit_sum').val(''); // Очистка поля, если значение некорректно
        }
    });

    // Обработка расчета кредита
    $('#Ok_credit').click(function() {
        const formData = new FormData(document.getElementById('CreditForm'));

        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('return_amount').value = data.total_payment.toFixed(2);
            document.getElementById('date_over').value = data.return_date;
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при расчете кредита.');
        });
    });

    // Логика для оформления кредита
    $('#Make_credit').click(function() {
        const formData = {
            fio: $('#fio').val(),
            passport: $('#passport').val(),
            birth_date: $('#birth_date').val(),
            credit_sum: $('#credit_sum').val(),
            interest_rate: $('#interest_rate').val(),
            time_credit: $('#time_credit').val(),
            car_brand: $('#car_brand').val(),
            car_model: $('#car_model').val(),
            car_year: $('#car_year').val()
        };

//        // Проверка обязательных полей перед отправкой запроса
//        if (!formData.fio || !formData.passport || !formData.birth_date || !formData.credit_sum ||
//            !formData.interest_rate || !formData.time_credit || !formData.car_brand ||
//            !formData.car_model || !formData.car_year) {
//            $('#resultMessage').text("Пожалуйста, заполните все обязательные поля!").css('color', 'red');
//            return;
//        }

        // Отправляем данные на сервер
        $.ajax({
            url: '/credit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                $('#resultMessage').text(response.message).css('color', 'green');
                $('#CreditForm')[0].reset(); // Очистить форму
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                $('#resultMessage').text('Произошла ошибка: ' + xhr.responseJSON.error).css('color', 'red');
            }
        });
    });
});
