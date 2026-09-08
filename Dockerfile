FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV DATABASE_PATH=/app/data/users_secure.db

WORKDIR /app

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup app.py entrypoint.sh ./

RUN chmod 0555 /app/entrypoint.sh \
    && mkdir -p /app/data \
    && chown -R appuser:appgroup /app/data

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3)"

ENTRYPOINT ["/app/entrypoint.sh"]