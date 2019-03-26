import json
import os

CONFIG_FILE = 'config.json'


def setup(email, token):
    config = {
        'email': email,
        'token': token
    }
    with open(CONFIG_FILE, 'w') as o:
        o.write(json.dumps(config, indent=2))
        print("Credentials saved to `{}`".format(CONFIG_FILE))

    return email, token


def read():
    email, token = None, None
    if os.path.isfile(CONFIG_FILE):
        print("Reading credentials from `{}`".format(CONFIG_FILE))
        with open(CONFIG_FILE, 'r') as f:
            config = json.loads(f.read())

        email = config.get('email')
        token = config.get('token')
    return email, token


if __name__ == '__main__':
    print(read())
