FROM python:3.6-alpine3.6

RUN apk --no-cache add build-base postgresql-dev  git \
    && git clone https://github.com/chakki-works/doccano \
    && cd doccano \
    && pip install -r requirements.txt \
    && rm -rf ~/.cache \
    && cd app/ \
    && python manage.py migrate \
    && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

EXPOSE 8000

WORKDIR doccano/app/

CMD python manage.py runserver 0.0.0.0:8000
