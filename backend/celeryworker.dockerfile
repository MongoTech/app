FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app/

RUN cd /app
RUN python3.9 -m venv venv
RUN . ./venv/bin/activate
RUN apt install gcc -y
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./app/pyproject.toml ./app/poetry.lock* /app/
RUN poetry install

ENV C_FORCE_ROOT=1

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
