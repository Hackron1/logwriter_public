import psycopg2
from flask import Flask, request, jsonify

import config

app = Flask(__name__)


def connect_to_database():
    ''' Создаем подключение к базе данных из конфигурационных параметров '''
    connection = psycopg2.connect(
        database=config.database_config['database'],
        user=config.database_config['user'],
        password=config.database_config['password'],
        host=config.database_config['host'],
        port=config.database_config['port']
    )
    return connection


@app.route('/logs', methods=['GET'])
def retrieve_logs():
    ''' Получаем логи из БД в зависимости от переданных параметров '''
    ip_address = request.args.get('ip', default=None)
    start_date = request.args.get('start_date', default=None)
    end_date = request.args.get('end_date', default=None)

    # Установка соединения с базой данных
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # Составление SQL запроса на выборку данных
    query = 'SELECT * FROM logs WHERE TRUE'
    if ip_address:
        query += f" AND server_ip = '{ip_address}'"
    if start_date:
        query += f" AND date_time >= '{start_date}'"
    if end_date:
        query += f" AND date_time <= '{end_date}'"

    cursor.execute(query)
    retrieved_logs = cursor.fetchall()

    # Преобразование результатов в формат JSON
    log_fields = ['log_ip', 'server_ip', 'date_time', 'log_query', 'response', 'weight']
    json_formatted_logs = []
    for log_entry in retrieved_logs:
        json_formatted_logs.append(dict(zip(log_fields, log_entry)))

    cursor.close()
    db_connection.close()

    return jsonify(json_formatted_logs)


if __name__ == '__main__':
    app.run(debug=True)
