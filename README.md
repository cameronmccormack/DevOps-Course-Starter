# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Trello Integration

The project uses the Trello API to store To Do items. A board must be set up in Trello with 3 lists for the app to use to store items of each status.

These board and list IDs must be defined (along with the API Key and Token) in the `.env` file. A list of required fields can be found in `.env.template`.

## Running the App

### Development mode

Once all of the dependencies have been installed, start the Flask app in development mode within a Docker container by running the following command:

```bash
$ docker-compose -f docker-compose.development.yml up --build
```

Alternatively, development mode can be run within the Poetry environment outside a container by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Production mode

Once all of the dependencies have been installed, start the Flask app in development mode within a Docker container by running the following command:

```bash
$ docker-compose up --build
```

## Running the App on the VM

On the control node, run the following:

```
 ansible-playbook playbook.yml -i ansible-inventory
```

## Test Coverage

Once all of the dependencies have been installed, all unit and integration tests can be run with:
```bash
$ poetry run pytest
```

Individual tests can be run with the keyword `-k` flag, for example:

```bash
$ poetry run pytest -k test_view_model_with_no_items
```

To set the tests to re-run on code changes, run:

```bash
$ poetry run ptw
```

To run the tests in a Docker container, run:

```bash
$ docker-compose -f docker-compose.test.yml up --build
```
 
 
To run the tests in a Docker container and set them to re-run on code changes, run:

```bash
$ docker-compose -f docker-compose.test-reload.yml up --build
```
