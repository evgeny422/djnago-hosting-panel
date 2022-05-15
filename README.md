# djnago-hosting-panel
Приложение которое решает проблему с обновления проектов из GIT на Django и поддержкой проектов.
Основной функционал:
  1)  подключение к репозиторию;
  2)  выполнение запроса к репозиторию(git pull);
  3)  возможность выполнения миграций;
  4)  обновление статики;
  5)  перезагрузка сервиса Gunicorn;
  6)  доступ к консоли.

Создать и активировать виртуальное окружение:
```
  python3 -m venv venv
  source venv/bin/activate 
```
Обновить pip до последней версии:
```
  python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
  pip install -r req.txt
```
Выполнить миграции:
```
  python3 manage.py migrate
  ```
Запустить проект:
```
  python3 manage.py runserver
```
