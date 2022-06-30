FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./app/pyproject.toml ./app/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/app
COPY --from=requirements-stage /tmp/requirements.txt /code/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY ./app/app /code/app/app
EXPOSE 8001
ENV PYTHONPATH "/code/app"
CMD ["python", "/code/app/app/main.py"]
