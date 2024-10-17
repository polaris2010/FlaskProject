$(document).ready(function() {
    // Обработчик нажатия кнопки "Проверить должника"
    $('#checkDebtor').on('click', function() {
        var fio = $('#fio').val().trim();
        var birth_date = $('#birth_date').val().trim();
        var passport = $('#passport').val().trim();

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
        var brand = $('#brand').val().trim();
        var model = $('#model').val().trim();
        var year = $('#year').val().trim();

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
                    var carPrice = parseFloat(response.avg_price);
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
                alert('Произошла ошибка: ' + (xhr.responseJSON ? xhr.responseJSON.error : 'Неизвестная ошибка'));
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
            $('#credit_sum').val('');
        }
    });

    // Обработка расчета кредита
    $('#Ok_credit').click(function() {
        const formData = new FormData(document.getElementById('CreditForm'));

        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сервера');
            }
            return response.json();
        })
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
            car_brand: $('#brand').val(),
            car_model: $('#model').val(),
            car_year: $('#year').val()
        };

        // Отправляем данные на сервер
        $.ajax({
            url: '/credit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                if (response.status === 'success') {
                    $('#resultMessage').text("Кредит оформлен, договор сформирован!").css('color', 'green');
                } else {
                    $('#resultMessage').text(response.message).css('color', 'red');
                }
            },
            error: function(xhr) {
                $('#resultMessage').text('Произошла ошибка при оформлении кредита').css('color', 'red');
                console.error('Ошибка:', xhr.responseText);
            }
        });
    });
});