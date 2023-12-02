FROM python:3.10-slim

WORKDIR /usr/src/app

EXPOSE 80

COPY . .

ENV PYTHONPATH /usr/src/app/src:${PYTHONPATH}

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]