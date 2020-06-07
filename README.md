# nlb-telegram-bot

## Setting Up

Get your API token from the `@BotFather` and copy it to a new file called `config.txt`
in the top-level project directory:

```
TOKEN = <your-token-here>
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
`docker exec -it <container-name> psql -U postgres`.

- `\l` to show all databases
- `\dt` to show all tables

#### Setting Up Locally

No guarantees that this will work with postgres. You're own your own.

``` sh
pipenv install
pipenv run python __init__.py
```
