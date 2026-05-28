FROM python:3.12-alpine

WORKDIR /app

# Устанавливаем только необходимые системные зависимости
RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]