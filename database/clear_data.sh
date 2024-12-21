#!/bin/sh

rm -r migrations/
rm development.db
sqlite3 development.db ".schema"
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
flask run_seeder