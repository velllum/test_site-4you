#### Тестовое задание / Junior Python Developer

## Простой REST-сервис на FastAPI.

### Список полей для модели пользователя:
- Идентификатор
- Имя
- Фамилия
- Отчество
- Email
- Пароль
- Дата и время создания
- Дата и время обновления

### Сервис должен реализовывать следующие операции:
- Добавление пользователя
- Обновление пользователя
- Удаление пользователя
- Получение списка пользователей
- Получение информации о пользователе по идентификатору
- Поиск пользователей по текстовым полям

### Проверки:
- Имя и фамилия пользователя обязательны для заполнения
- Email должен быть уникальным среди всех пользователей
- Пароль должен содержать не менее 6 символов и содержать хотя бы одну цифру и
одну букву.

### Требования:
- Код в репозитории на GitHub
- Управление зависимостями проекта через pipenv
- Работа с БД через SQLAlchemy. Структура БД должна создаваться через миграции с
помощью Alembic
- Получение настроек через переменные окружения.
- Наличие юнит-тестов на pytest или unittest будет плюсом.