CONFIG_FILE = 'config.txt'

configs = {}
with open(CONFIG_FILE, 'r') as f:
    for line in f:
        key, val = line.split('=')
        key, val = key.strip(), val.strip()
        configs[key] = val

token = configs['TOKEN']
