FROM python:3.10.4-slim-buster as base
RUN pip install poetry
EXPOSE 5000
WORKDIR /app
COPY . /app/
RUN poetry install --no-root --no-dev

FROM base as prod
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

FROM base as dev
ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
