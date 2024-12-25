FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl postgresql-client

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install

COPY . .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]