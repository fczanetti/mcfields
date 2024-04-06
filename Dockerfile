ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# RUN mkdir -p /code

# WORKDIR /code

ARG DEV_LIBS
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system ${DEV_LIBS}

# COPY . /code
COPY . ./

EXPOSE 8000

# TODO: replace demo.wsgi with <project_name>.wsgi
ENTRYPOINT ["./start.sh"]
