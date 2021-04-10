from .api import init, app
from dotenv import load_dotenv
import os
import logging


def check_env():
    logging.info(f'checking env variables...')
    envs = dict()
    envs['domain'] = os.getenv('DOMAIN')
    logging.debug(f'domain: {envs["domain"]}')

    envs['region_id'] = os.getenv('REGION_ID')
    logging.debug(f'region_id: {envs["region_id"]}')

    envs['access_key_id'] = os.getenv('ACCESS_KEY_ID')
    logging.debug(f'access_key_id: {envs["access_key_id"]}')

    envs['access_secret'] = os.getenv('ACCESS_SECRET')
    logging.debug(f'access_secret: {envs["access_secret"]}')

    envs['token'] = os.getenv('TOKEN')
    logging.debug(f'token: {envs["token"]}')
    assert (None not in envs.values())
    return envs


def main(host='0.0.0.0', port=9401, debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    # load env vars from .env file
    load_dotenv(dotenv_path='.env')

    # check all required env vars
    envs = check_env()

    # init restful server
    init(envs)

    # run restful server
    app.run(host=host, port=port, debug=debug)
