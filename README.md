# djnago-hosting-panel
Приложение которое решает проблему с обновления проектов из GIT на Django и поддержкой проектов.
Основной функционал:
  1)  подключение к репозиторию;
  2)  выполнение запроса к репозиторию(git pull);
  3)  возможность выполнения миграций;
  4)  обновление статики;
  5)  перезагрузка сервиса Gunicorn;
  6)  доступ к консоли.

Для перезагрузки сервисов nginx и gunicorn необходимо создать переменную окружения secret_key, значение которой, соответствует паролю sudo:
```
nano ~/.bashrc
export secret_key= пароль sudo
source ~/.bashrc
```

Создать и активировать виртуальное окружение:
```
  python3 -m venv venv
  source venv/bin/activate 
```
Установить зависимости:
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
