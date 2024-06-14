установка: для того чтоб все заработало надо создать постгрес бд и настроить его используя команды ниже:
(sql)
create table if not exists logs
(
	log_ip uuid default uuid_generate_v4() constraint pk_log_ip primary key, 
	server_ip text not null default 'нет данных',
	date_time text not null default 'нет данных',
	log_query text not null default 'нет данных',
	response text not null default 'нет данных',
	weight text not null default 'нет данных'
);

Описание работы:

init_export - экспорт данных из лог файла в бд (запуск в main.py)
select_logs показ всех данных из бд (запуск в main.py)
select_logs date_time weight 
select_logs 2004.04.14 
select_logs 2004.04.14 2023.08.23 (дата от до)
select_logs date_time 2004.04.14 weight 2023.08.23 (дата от до + вес)

(по факту можно вызвать с любыми параметрами из бд)

api файл дает доступ через веб строку к получению json файлов по фильтру


'%h': 'IP-адрес клиента',
'%t': 'Время запроса в формате',
'%r': 'Первая строка запроса',
'%>s': 'Статус ответа сервера',
'%b': 'Размер ответа в байтах'

файл gen_log.py используется в ручную для экспериментов с логами (простыми словами это генератор логов)


web_api
http://127.0.0.1:5000/logs
http://127.0.0.1:5000/logs
http://127.0.0.1:5000/logs?ip=192.168.1.1
http://127.0.0.1:5000/logs?start_date=2024-06-01&end_date=2024-06-13