# ParsMailLog
Для запуска скрипта с сохраненим данных, запускаем main:
python main.py

либо run main из IDE

Данны загружаются из файла (база уже должна существовать, параметры подключения лежат в файле
/backend/constants.py)

Для запуска сервера используем uvicorn:
uvicorn main:app --reload

Для обращения к странице с примером используем {ip}/index

Команда ===Применить прекоммит=== не стал добавлять в хуки:
poetry run pre-commit run --all-files



