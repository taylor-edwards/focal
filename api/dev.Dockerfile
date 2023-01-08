FROM python:3
MAINTAINER Taylor Edwards (taylor@focal.pics)

WORKDIR /api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV development
CMD ["python", "app.py"]
