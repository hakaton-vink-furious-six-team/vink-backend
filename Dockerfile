FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
