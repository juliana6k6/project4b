FROM python:3

WORKDIR / materials

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .