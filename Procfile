web: cd api; newrelic-admin run-program gunicorn project.wsgi -b "0.0.0.0:$PORT" --workers=4 --settings=envs.live
beat: cd api; newrelic-admin run-program python manage.py celery beat --settings=envs.live
celery: cd api; newrelic-admin run-program python manage.py celery worker -c 4 -Q celery --settings=envs.live
push: cd api; newrelic-admin run-program python manage.py celery worker -c 4 -Q push --settings=envs.live
analytics: cd api; newrelic-admin run-program python manage.py celery worker -c 4 -Q analytics --settings=envs.live
logging: cd api; newrelic-admin run-program python manage.py celery worker -c 4 -Q logging --settings=envs.live

