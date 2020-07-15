import logging
import sys

##################
## Config files ##
##################

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

#############
## Logging ##
#############

## Logging will mainly be used in db helpers; I don't want to clog up the handlers

LOGNAME = 'bot.log'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logFormatter = logging.Formatter('%(asctime)s - %(name)s [%(levelname)s] %(message)s')

fileHandler = logging.FileHandler(LOGNAME)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)
