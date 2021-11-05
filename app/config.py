from decouple import config


class AppConfig:
    APP_NAME = config("APP_NAME")
    APP_VERSION = config("APP_VERSION")
    APP_PATH = config("APP_PATH")
    DOCS_URL = config("DOCS_URL")
    APP_DESCRIPTION = config("APP_DESCRIPTION")
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = config("ALG")
