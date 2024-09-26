$(document).ready(function() {
    $('#fio').on('input', function() {
        // Приводим первую букву к заглавной, а остальные буквы к строчным
        let fio = $(this).val().toLowerCase();
        fio = fio.charAt(0).toUpperCase() + fio.slice(1);
        $(this).val(fio);
    });
});

    $('#calculateLoan').click(function () {
        var formData = $('#loanForm').serialize();

        $.post('/calculate_loan', formData, function (response) {
            $('#return_amount').val(response.return_amount);
        }).fail(function (response) {
            alert(response.responseJSON.error);
        });
    });

    $('#loanForm').submit(function (event) {
        event.preventDefault();  // Останавливаем стандартное поведение формы

        var formData = $(this).serialize();

        $.post('/submit_loan', formData, function (response) {
            alert(response.message);
        }).fail(function (response) {
            alert(response.responseJSON.error);
        });
    });
});
