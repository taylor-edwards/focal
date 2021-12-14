FROM python:3
MAINTAINER Taylor Edwards (taylor@focal.pics)

RUN python -m pip install --upgrade pip

WORKDIR /api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --gecos "" --disabled-password --no-create-home --uid 1000 flask
RUN chown -hR flask:flask .
USER flask
CMD ["uwsgi", "--ini", "uwsgi.ini", "--enable-threads"]
