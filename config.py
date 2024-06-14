# Файл config.py
# Конфигурационные настройки для системы логирования

# Пути к файлам логов и форматы их строк
log_files = [
    ('C:/Users/ivanm/PycharmProjects/logwriter_/logs1.txt', '%h,%t,%r,%>s,%b')
]

# Информация для подключения к базе данных
database_config = {
    'database': 'writer',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}
