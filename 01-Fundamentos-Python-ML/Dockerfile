FROM python:3.12-slim

WORKDIR /app

COPY requirements-api.txt .

RUN pip install --no-cache-dir -r requirements-api.txt

COPY exercicios/ ./exercicios/
COPY dados/consumo_energetico_v1.csv ./dados/consumo_energetico_v1.csv

EXPOSE 8000

CMD ["uvicorn", "exercicios.api_energia:app", "--host", "0.0.0.0", "--port", "8000"]
