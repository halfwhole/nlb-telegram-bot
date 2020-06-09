CONFIG_FILE = '.env'

configs = {}
with open(CONFIG_FILE, 'r') as f:
    for line in f:
        key, val = line.split('=')
        key, val = key.strip(), val.strip()
        configs[key] = val

token = configs['TOKEN']
postgres_user = configs['POSTGRES_USER']
postgres_password = configs['POSTGRES_PASSWORD']
postgres_db = configs['POSTGRES_DB']
conn_string = 'postgresql+psycopg2://%s:%s@db:5432/%s' % (postgres_user, postgres_password, postgres_db)
