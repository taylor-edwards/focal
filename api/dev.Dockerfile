FROM python:3
MAINTAINER Taylor Edwards (taylor@focal.pics)

WORKDIR /api
ENV PATH /api/.venv/bin:$PATH
ENV FLASK_ENV development
CMD ["python", "app.py"]
