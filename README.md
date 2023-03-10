Клиент-серверное приложение на Flask (Python 3.9.7)

Функционал сервер:

    База данных:
        - yml-файл
        - Redis

    Endpoint GET:
        - Возвращает все соответствия из БД
    Endpoint POST:
        - Принимает длинную ссылку и метод шифрования 'uuid4' или 'timestamp', 
            генерирует 6  уникальных символов для ссылки)
        - Возвращает сгенерированную короткую ссылку.
    
    Дополнительно:
        - Обработка не существующей страницы
        - Обработка страницы redirect
        - Проверка ссылки на существование
        - При добавлении новой ссылки проверяется есть или она уже в базе


Функционал Клиент:

    Страница Главная:
        - Отображает форму для сокращения ссылки:
            Поле для вставки ссылки
            Меню выбора метода шифрования
            Кнопка "Сократить" для генерации короткой ссылки
        
        - Отображает таблицу всех существующих ссылок в БД:
            №, Ключ, Значение
    
    Страница Переадресации:
        - Отображает таймер через которое будет выполен redirect
        - Отображает блок рекламы
    
    Страница 404:
        - Отображает сообщение об ошибке 404



Запуск приложения:

#### При помощи `docker-compose`

1. Склонировать проект:

`git clone [URL] [DIR]`

2. Перейти в директорию проекта

`cd [DIR]`

3. Ввести команду в терминале:

`docker-compose up --build`

4. Сервер автоматически запустится и будет доступен в браузере по адресу:
`http://127.0.0.1:5000/`
или 
`http://localhost:5000/`

5. Данные сохраняются в примонтированный `volume`


#### Настройки
В файле `docker-compose` значение переменной **STORAGE_TYPE**
может быть двух типов:

`STORAGE_TYPE: redis`
 или 
`STORAGE_TYPE: yaml`



