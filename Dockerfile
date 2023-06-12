FROM python:3.11.3

RUN mkdir /src
WORKDIR /src

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev

RUN chmod a+x docker/*.sh