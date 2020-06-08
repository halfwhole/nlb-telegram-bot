# nlb-telegram-bot

## Setting Up

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

#### Setting Up with Docker (recommended)

Install `docker-ce` and `docker-compose` with your preferred package manager,
then run `docker-compose up`:

``` sh
sudo apt install docker-ce
sudo apt install docker-compose
docker-compose up [-d]
```

This will start two containers, one for the telegram bot and one for the postgres database.

To run `psql` in the postgres container, use
`docker exec -it <container-name> psql -U <postgres-user>`.

- `\l` to show all databases
- `\dt` to show all tables

#### Setting Up Locally

No guarantees that this will work with postgres. You're own your own.

``` sh
pipenv install
pipenv run python __init__.py
```
