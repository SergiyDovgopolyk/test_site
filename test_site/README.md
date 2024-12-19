# How to use this project


## Installation

Activate your virtual environment and follow the instructions below:
for Windows:
```Shell
  python -m venv venv
  venv\Scripts\activate
```
for MacOS and Linux:
```Shell
  python3 -m venv venv
  source venv/bin/activate
```
Or with poetry:
```Shell
  poetry install
  poetry shell
```

- Install dependencies.
```Shell
  pip install -r requirements.txt
```
*or with poetry*
```Shell
  poetry install
```

# ЗАПУСК:
```Shell
  python3 main.py
  ```



## Что реализовано в api_test_site/bad
1) Ошибки с длиной заголовков, тайтлов, дублями и т.д. подписаны на каждой странице статей
    1.1) По адресу http://127.0.0.1:7000/category/culture/article/33 откроется страница с ошибкой 500
2) Нижний реестр в URL реализован на странице "About Us" (в футере)
3) URL с кириллицей реализован на странице "Контакты" (в футере)
4) Длинный URL (более 115 символов) реализован на странице "Long URL Page"
5) Для страниц "About Us" и "Контакты" не реализована каноническая ссылка. Для страницы "Long URL Page" - каноническая ссылка пустая
6) Для страницы категорий статей отсутствует разметка Open Graph
7) Для страницы 'News' не реализован атрибут hreflang
8) Добавлен фай "robots.txt" в папку со статическими файлами (http://127.0.0.1:7000/robots.txt)
9) Для страницы "Long URL Page" и страницы с категориями статтей не реализована Микроразметка Schema.org (реализована в шаблонах)
10) Для страницы "Long URL Page" реализован долгий ответ от сервера (больше 400 миллисекунд)
11) На главную страницу не редиректит по маршруту https://127.0.0.1:7000/index.html - (специально упущенное условие). Откроется дубль главной страницы
12) Все страницы, кроме "News", редиректит на HTTPS. News работает на HTTP