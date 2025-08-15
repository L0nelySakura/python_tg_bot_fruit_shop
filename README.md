# python_tg_bot_fruit_shop
Телеграм бот с функционалом добавления информации о продаже фруктов в определённом магазине, а также с функцией генерирования плана продаж за определённый месяц.
## Технологии
- [Python](https://www.python.org/)

## Использование
### Требования
Установите зависимости, указанные [выше](#Технологии)
### Установка и запуск сервиса

1) Скачайте репозиторий: 
```sh
git clone https://github.com/L0nelySakura/python_tg_bot_fruit_shop
```

2) Перейдите в папку проекта:
```sh
cd python_tg_bot_TK_RF
```

3) Установите библиотеки при помощи
```
pip install -r requirements.txt
```

3) Настройте .env файл исходя из примера (.env.example), скачайте json-файл с Google Cloud Console (Create Credentials -> Service Account; Add Key -> Create new key -> JSON), переименуйте его в credentials.json
  
4) Запуск проекта:
```sh
python main.py
```

После запуска перейдите в telegram на аккаунт бота и нажмите /start
