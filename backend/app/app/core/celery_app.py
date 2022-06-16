from celery import Celery  # type: ignore

options = "authSource=admin&retryWrites=true&w=majority"
celery = Celery('EOD_TASKS', broker=f'mongodb://admin:devpass@mongo:27017/fastapi?{options}')
