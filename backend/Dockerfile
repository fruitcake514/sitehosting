FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set permissions for mounted volumes
ARG HOST_UID
ARG HOST_GID
RUN groupadd -g ${HOST_GID:-1000} appgroup && \
    useradd -r -u ${HOST_UID:-1000} -g appgroup appuser && \
    chown -R appuser:appgroup /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]