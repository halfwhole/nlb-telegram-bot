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
