#stage 1
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#stage 2
FROM python:3.9-alpine

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
