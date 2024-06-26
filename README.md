# YaCut

> Сервис для укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологии проекта

- Python — высокоуровневый язык программирования.
- Flask — веб-фреймворк для разработки веб-приложений.
- SQLite — это встраиваемая система управления базами данных для клиент-серверных приложений.
- SQLAlchemy — это программная библиотека на языке Python для работы с реляционными СУБД с применением технологии ORM.
- Alembic — это инструмент для миграции базы данных, используемый в SQLAlchemy.
- WTForms– библиотека, способная генерировать формы, проверять их, наполнять начальной информацией и др.

### Как запустить проект:

Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:V1olenceDev/yacut.git
```

```
cd yacut
```

Cоздайте и активируйте виртуальное окружение:

```
python -m venv venv
```

```
. venv/Scripts/activate
```

Установите зависимости из файла `requirements.txt`:

```
python -m pip install --upgrade pip
```


```
pip install -r requirements.txt
```

Создайте `.env` файл с переменными окружения:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Выполните миграции:

```
flask db upgrade
```

Запустите сервис на веб-сервере разработки Flask:

```
flask run
```

## Автор
[Гаспарян Валерий Гургенович](https://github.com/V1olenceDev)
