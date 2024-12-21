#!/bin/sh

. set_envpro.sh
rm -r migrations/
flask --app 'app:create_app(config_class="config.Production")' db init
flask --app 'app:create_app(config_class="config.Production")' db migrate -m "Initial migration."
flask --app 'app:create_app(config_class="config.Production")' db upgrade
flask --app 'app:create_app(config_class="config.Production")' run_seeder