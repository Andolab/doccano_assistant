FROM python:3.6-alpine3.6

COPY app/ app/
COPY requirements.txt app/
WORKDIR app/

RUN apk --no-cache add build-base \
    && apk --no-cache add postgresql-dev \
    && pip install -r requirements.txt \
    && rm -rf ~/.cache \
    && python manage.py migrate \
    && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
