import random
from datetime import datetime, timedelta


# Функция для генерации случайного IP-адреса
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# Функция для генерации случайной даты в заданном диапазоне
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime('%d/%b/%Y:%H:%M:%S')


# Определение начальной и конечной даты для генерации
start_date = datetime.strptime("01/Jan/2020", "%d/%b/%Y")
end_date = datetime.strptime("31/Dec/2020", "%d/%b/%Y")

# HTTP методы и URL пути
methods = ["GET", "POST", "DELETE", "PUT"]
urls = ["/home/", "/about/", "/api/data/", "/hidden/", "/login/"]

# Статусы HTTP и размер ответа
statuses = [200, 404, 500, 403, 301]
sizes = [128, 256, 512, 1024, 2048, 4096]

# Генерация 100 логов
logs = []
for _ in range(100):
    ip = random_ip()
    date = random_date(start_date, end_date)
    method = random.choice(methods)
    url = random.choice(urls)
    status = random.choice(statuses)
    size = random.choice(sizes)
    log = f"{ip} - - [{date} -0300] \"{method} {url} HTTP/1.0\" {status} {size}"
    logs.append(log)

# Вывод сгенерированных логов
for log in logs:
    print(log)
