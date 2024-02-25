FROM python:3.10

WORKDIR /api
ADD . /api

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "asgi:app", "--host", "127.0.0.1", "--port", "5000"]
