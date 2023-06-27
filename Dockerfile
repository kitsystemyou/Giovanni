FROM python:3.11.4-slim-bookworm

RUN pip install --upgrade pip
COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8080

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]