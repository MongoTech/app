from celery import Celery

MONGO_USER = "root"
MONGO_PASS = "mongo"
MONGO_HOST = "localhost"
MONGO_DB = "answeron"
options = "authSource=admin&retryWrites=true&w=majority"
celery = Celery('EOD_TASKS', broker=f'mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/{MONGO_DB}?{options}')
