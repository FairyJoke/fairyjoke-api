FROM python:3.11 AS requirements

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

FROM requirements AS app

COPY src /app/src

CMD ["python", "-m", "src.fairyjoke"]