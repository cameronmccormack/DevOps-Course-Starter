#!/bin/bash
poetry run gunicorn wsgi --bind 0.0.0.0:5000
