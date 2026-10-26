FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data outputs/images plugins

# BYOI mode: respond with JSON on every /v1/chat/completions call so RAG
# planners (OnDemand, etc.) that pass system prompts expecting JSON don't
# break. Set to "false" to disable (regular chat remains plain text).
ENV NAGRO_ALWAYS_JSON=true

EXPOSE 8000

CMD ["python", "run.py"]
