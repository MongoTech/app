from celery import Celery

options = "authSource=admin&retryWrites=true&w=majority"
celery = Celery('EOD_TASKS', broker=f'mongodb://admin:devpass@localhost:27017/fastapi?{options}')
