# Servers-test

Добрый день!

Если есть желание запустить тесты локально  необходимо установить интерпретатор языка python 
и настроить виртуальное окружение.

Для этого необходимо зайти в настройки Pycharm → Python Interpreter и выбрать доступный вам интерпретатор языка. 
Если его нет установите python через тут - https://www.python.org/

Версия Python должна быть 3.9

После выбора интерпретатора жмём Apply и ждём пока IDE настроит и применит изменения

Необходимо активировать виртуальное окружение командой source venv/bin/activate, если вдруг ide не сделало это 
автоматически

Также необходимо, чтобы был установлен chromdriver - https://chromedriver.chromium.org/downloads
А также был запущен selenium 

В файле requirements.txt содержатся все необходимые зависимости. Их можно установить через ide или командой 
pip install -r requirements.txt

Также необходимо в файле .env_example вбить свои креды и переименовать файл в .env

Тесты запускаются командой python -m pytest tests/дальнейший путь до директории/файла
Отдельный тест можно запустить с ключом -k, например python -m pytest tests/ui_tests/profile_tests/ -k имя теста


Примечание: 

Я не стал углубляться в тест-дизайн, а решил делать основные проверки. 
Также в реальной жизни ассертов в тестах было бы значительно больше. 

Методы на редактирование профиля и создания сервера гибкие, при их вызове можно передавать любые значения в инпуты,
выбирать любые чекбоксы. Таким образом за счет параметризации можно в рамках одного теста проверять множество сценариев.

Тесты проходят. В один поток: 16 passed, 1 skipped in 208.13s (0:03:28)
Тесты изолированы друг от друга, так что при небольших правках их легко можно запускать в несколько потоков

В реальных условиях я бы предпочел удалять сущности, созданные в тесте, через бд. Здесь реализовывать ручное удаление
не стал. 

Ассертов минимальное количество. В реальных условиях их было-бы значительно больше. 

