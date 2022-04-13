
FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install pylama pytest pytest-cov requests black bandit

RUN pip install -e .