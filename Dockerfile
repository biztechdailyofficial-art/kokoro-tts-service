FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Bake Kokoro's model weights into the image at build time. Without this,
# the container downloads them from Hugging Face on first boot, which
# (combined with gunicorn's worker timeout) can take longer than
# Railway's healthcheck window and fail the deploy.
RUN python -c "from kokoro import KPipeline; KPipeline(lang_code='a'); KPipeline(lang_code='b')"

ENV PORT=8080
ENV HF_HUB_OFFLINE=1
EXPOSE 8080

# Shell form (not exec/JSON-array form) so $PORT actually expands -
# Railway injects its own PORT value and routes the healthcheck there.
CMD gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 300 app:app
