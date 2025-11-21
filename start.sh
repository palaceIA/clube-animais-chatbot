#!/bin/bash

if [ ! -f "/tmp/models/multilingual-e5-large/config.json" ]; then
    echo "Baixando modelo intfloat/multilingual-e5-large para /tmp/models/multilingual-e5-large ..."
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('intfloat/multilingual-e5-large').save('/tmp/models/multilingual-e5-large')"
fi

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file .env