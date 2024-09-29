$(document).ready(function() {
    // Обработка проверки должника
    $('#checkDebtor').click(function() {
        var fio = $('#fio').val();
        var birth_date = $('#birth_date').val();
        var passport = $('#passport').val();

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
                    $('#resultMessage').text('В кредите отказано');
                } else {
                    $('#resultMessage').text('Кредит можно выдать');
                }
            },
            error: function(xhr) {
                $('#resultMessage').text('Произошла ошибка: ' + xhr.responseJSON.error);
            }
        });
    });

    // Обработка расчета стоимости авто
    $('#calculatePrice').click(function() {
    var brand = $('#brand').val();
    var model = $('#model').val();
    var year = $('#year').val();

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
            console.log(response); // Для отладки
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
            console.error(xhr.responseText); // Для отладки
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
        .catch(error => console.error('Ошибка:', error));
    });

    // Логика для оформления кредита
    $('#Make_credit').click(function() {
        alert('Кредит успешно оформлен!');
    });
});
