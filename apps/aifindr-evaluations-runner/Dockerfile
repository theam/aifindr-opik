FROM 095325195762.dkr.ecr.eu-west-1.amazonaws.com/golden-images/python-base:latest AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=nonroot:nonroot . .

FROM builder AS runner

WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"] 