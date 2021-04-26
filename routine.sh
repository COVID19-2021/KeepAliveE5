#!/usr/bin/env bash

[ -f 'config/app.json' ] || exit

poetry run python crypto.py d
poetry run python task.py
poetry run python crypto.py e
