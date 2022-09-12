FROM python:3.10.4-slim-buster as base
RUN pip install poetry
EXPOSE 5000
WORKDIR /app
COPY poetry.lock poetry.toml pyproject.toml /app/
RUN poetry install --no-root --no-dev

FROM base as prod
COPY . /app/
RUN chmod +x ./entrypoint.sh
CMD poetry run gunicorn wsgi --bind "0.0.0.0:${PORT:-5000}"

FROM base as dev
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]

FROM base as test-reload
ENTRYPOINT ["poetry", "run", "ptw", "--poll"]

FROM base as test
COPY . /app/
ENTRYPOINT ["poetry", "run", "pytest"]
