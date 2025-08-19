from os import getenv, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))

SSH_REMOTE_HOST = getenv("SSH_REMOTE_HOST")
SSH_USERNAME = getenv("SSH_USERNAME")
SSH_PASSWORD = getenv("SSH_PASSWORD")
SSH_FILEPATH = getenv("SSH_FILEPATH")
SSH_KEY_FILEPATH = getenv("SSH_KEY_FILEPATH")
SSH_COMMAND = getenv("SSH_COMMAND")
DESTINATION_FOLDER = getenv("DESTINATION_FOLDER")
