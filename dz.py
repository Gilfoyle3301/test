import requests
from bs4 import BeautifulSoup
import psycopg2
#Подключение к созданной базе данных newspaper под пользователем jony

connection = psycopg2.connect(
  database="newspaper", 
  user="postgres", 
  password="12345", 
  host="172.10.1.10", 
  port="4000"
)
connection.autocommit = True
print("Database opened successfully")
#Генерация таблицы 
cursor = connection.cursor()
def table():  
    cursor.execute('''CREATE TABLE news(
        id serial PRIMARY KEY,
        time_s varchar(20),
        news TEXT NOT NULL,
        link varchar(255));''')
    return print("Table created successfully")
#Запуск парсера и занос данных в БД
def scapper():
    url = 'https://www.vesti.ru'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    news = [ (new.text).strip() for new in soup.find_all('h3', class_ = "main-news__title")]
    links = [ a.get('href') for a in soup.find_all('a', class_= "main-news__pic-wrapper") ]
    time = [(t.text).strip() for t in soup.find_all('div', class_ = 'main-news__time')]
    for t, n, l  in zip(time, news, links):
        cursor.execute("INSERT INTO news (time_s,news,link) VALUES (%s,%s,%s)", (t, n, url+l))
    connection.close()
#Экспорт в CSV
def csv():
    sql = "COPY (SELECT * FROM news) TO STDOUT WITH CSV DELIMITER ';'"
    with open("/tmp/table.csv", "w") as file:
        cursor.copy_expert(sql, file)
    connection.close()
    return print("extracted table successfully")

go = str(input("Выберете действие:\n1.Cгенерировать таблицу\n2.Запустить парсер новостей\n3.Экспортировать таблицу\n"))
if go == str(1):
   table()
elif go == str(2):
    scapper()
elif go == str(3):
    csv()
else:
    print("Unknotion action")
