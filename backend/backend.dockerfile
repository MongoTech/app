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

COPY ./app /app
ENV PYTHONPATH=/app
