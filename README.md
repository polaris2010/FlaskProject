Сайт Autocredit проверяет заемщика на наличие долгов, анализирует заявку и рассчитывает сумму кредита под залог автомобиля на основе парсинга объявлений Авито:

- создан на основе библиотеки Flet;
- проверяет по ФИО не является ли заявитель должником, выполняет валидацию вводимых данных;
- определяет среднюю рыночную цену предлагаемого в залог автомобиля путем парсинга объявлений, размещенных на Avito;
- рассчитывает возможную сумму кредита по заданному дисконту и сумму к погашению;
- передает сведения о заемщике и выдаче кредита в БД SQlite3;
- при оформлении кредита формирует txt файл с договором и данными заемщика.
