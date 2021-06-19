FROM python:3-alpine

WORKDIR /usr/src/app

ENV FLASK_APP=handler.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
