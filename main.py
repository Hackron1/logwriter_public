import datetime
import re

import config  # Импорт файла конфигурации
from sender import read_data, data_patterns, init_connection, pull_data


def build_query(user_input: [str]) -> str:
    '''Генерируем динамический SQL запрос на основе ввода пользователя'''
    user_input = user_input.split(' ')
    date_regex = re.compile(r'\d{4}(-\d{2}){2}')  # Регулярное выражение для формата даты
    date_list = []
    selected_columns = ''
    unrecognized_items = []  # Список для хранения неопознанных элементов ввода
    for item in user_input:
        if date_regex.match(item) and len(date_list) < 2:  # Проверка на дату, максимум две даты
            date_list.append(item)
        elif item in ['log_ip', 'server_ip', 'date_time', 'log_query', 'response',
                      'weight'] and item not in selected_columns:
            # Проверка соответствия элемента одному из столбцов БД
            if selected_columns == '':
                selected_columns += item
            else:
                selected_columns += ', ' + item
        elif item != 'select_logs':  # Остальное добавляем в список нераспознанного
            unrecognized_items.append(item)
    if selected_columns == '':
        selected_columns = '*'  # Если столбцы не указаны, выбираем все
    query = 'select ' + selected_columns + ' from logs'
    where_clause = ''
    if len(date_list) == 1:
        # Если указана одна дата, формируем условие выборки
        date1 = list(map(int, date_list[0].split('.')))
        where_clause = f' where date_time > TO_DATE(\'{date1[0]}/{date1[1]}/{date1[2]}\', \'YYYY/MM/DD\') and date_time < CURRENT_DATE'
    elif len(date_list) == 2:
        # Если указаны две даты, сравниваем их
        date1 = list(map(int, date_list[0].split('.')))
        date2 = list(map(int, date_list[1].split('.')))
        if datetime.date(date1[0], date1[1], date1[2]) < datetime.date(date2[0], date2[1], date2[2]):
            where_clause = f' where date_time > TO_DATE(\'{date1[0]}/{date1[1]}/{date1[2]}\', \'YYYY/MM/DD\') and date_time < TO_DATE(\'{date2[0]}/{date2[1]}/{date2[2]}\', \'YYYY/MM/DD\')'
        else:
            where_clause = f' where date_time > TO_DATE(\'{date2[0]}/{date2[1]}/{date2[2]}\', \'YYYY/MM/DD\') and date_time < TO_DATE(\'{date1[0]}/{date1[1]}/{date1[2]}\', \'YYYY/MM/DD\')'
    query += where_clause + ';'
    if unrecognized_items:
        # Показываем пользователю неопознанные элементы
        print(f'Неопознанные элементы: {unrecognized_items}')
    return query, selected_columns  # Возвращаем запрос и выбранные столбцы для дальнейшего вывода


def fetch_data_from_db(user_input, connection) -> list[dict[str, str]]:
    '''Отправляем запрос в БД и получаем данные'''
    query, selected_columns = build_query(user_input)
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    json_result = []
    if selected_columns.strip() == '*':
        selected_columns = ['log_ip', 'server_ip', 'date_time', 'log_query', 'response', 'weight']
    else:
        selected_columns = [col.strip() for col in selected_columns.split(',')]

    for log in result:
        json_format = {}
        if len(log) != len(selected_columns):
            print(selected_columns, log)
            raise ValueError("Количество столбцов и элементов в результате не совпадает")
        for i, column in enumerate(selected_columns):
            json_format[column] = str(log[i])
        json_result.append(json_format)

    return json_result


try:
    connection = init_connection(config.database_config)
    if connection is None:
        raise Exception
    while True:
        user_input = input('Enter the command: ')
        if 'init_export' in user_input:
            # Отправка данных в БД
            logs = read_data(config.file_paths, data_patterns)
            logs = list(map(tuple, logs))
            pull_data(connection, logs)
        elif 'select_logs' in user_input:
            # Выборка данных из БД
            logs = fetch_data_from_db(user_input, connection)
            for log in logs:
                print(log)
        else:
            print('Неопознанная команда')
except KeyboardInterrupt:
    print('Сессия завершина')
