# nlb-telegram-bot

## Setting Up

#### Environment file

Create a new file `.env` in the top-level project directory with the
following configurations:

- `TOKEN`: Telegram API token from the `@BotFather`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

```
# Example .env file
TOKEN = <your-token-here>
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_DB = nlb
```

#### Docker

Both `docker` and `docker-compose` will need to be installed.

Run `docker-compose up`, which will start two containers&mdash;one for for the python
telegram bot, and one for the postgres database:

``` sh
docker-compose up [-d]
```

- To access the python bot container, use `docker exec -it <container-name> bash`.
- To access postgres, use `docker exec -it <container-name> psql -U <postgres-user> nlb`.

## Using Alembic

For more details, see the [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html).

#### Creating a migration

``` sh
pipenv run alembic revision -m "Create a new migration"
```

#### Upgrading/downgrading migrations

Remember to run the following commands from within the python docker container,
if you're using one:

``` sh
pipenv run alembic upgrade head  # Upgrade to latest version
pipenv run alembic upgrade +1    # Upgrade by 1 migration
pipenv run alembic downgrade -1  # Downgrade by 1 migration
```

## Using SQLAlchemy

For more details, see the [SQLAlchemy tutorial](https://docs.sqlalchemy.org/en/13/orm/tutorial.html).

Here's a sampling of what you can do with SQLAlchemy:

``` python
book = Book(bid=123, user_id=1337, title='TITLE', author='AUTHOR')
session.add(book)
session.commit()
session.delete(book)
session.rollback()

session.query(Book).all()
session.query(Book).first()

availability = Availability(
    book_id=book.id,
    branch_name='BRANCH',
    call_number='CALL',
    status_desc='STATUS',
    shelf_location='SHELF'
)
session.add(availability)
session.commit()

book.availabilities
# [<Availability(id=1, book_id=1, branch_name='BRANCH', status_desc='STATUS')]
availability.book
# <Book(id=1, bid=123, user_id=1337, title='TITLE', author='AUTHOR')
```

#### Running the python console

Again, the console should be run from within the python docker container:

``` sh
pipenv run python -i models.py
```

All of the above python code can be executed as-is from within the console.

## Developer notes

If you need to install or uninstall python packages:

``` sh
pipenv [un]install <package>
docker-compose build
```
