#!/bin/bash

python scripts_for_start/wait_for_db.py

python scripts_for_start/run_migrations.py

python scripts_for_start/collect_static.py

python scripts_for_start/create_superuser.py

python scripts_for_start/load_test_data.py

exec python manage.py runserver 0.0.0.0:8000