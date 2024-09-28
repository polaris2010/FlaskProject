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
                    $('#resultMessage').text('Кредит выдать');
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
                if (response.status === 'success') {
                    // Устанавливаем стоимость авто в поле
                    $('#carPrice').val(response.avg_price + ' руб.');
                } else {
                    alert('Ошибка: ' + response.message);
                }
            },
            error: function(xhr) {
                alert('Произошла ошибка: ' + xhr.responseJSON.error);
            }
        });
    });
});
