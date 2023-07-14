from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")

SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_AUTH_RESET = os.environ.get("SECRET_AUTH_RESET")
SECRET_AUTH_VERIF_TOKEN = os.environ.get("SECRET_AUTH_VERIF_TOKEN")
