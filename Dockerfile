FROM python:3.10-slim

WORKDIR /app

ENV PORT=80

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "server.py"]
