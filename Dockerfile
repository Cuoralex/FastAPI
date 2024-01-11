# Etapa de construcción
FROM python:3.10.12-slim AS development_build

WORKDIR /code

COPY requirements.txt .

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        gcc \
        curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc curl \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY . .

# Variables de entorno
ENV WEBAPP_DIR=/code/app \
    STATUS_ENV=${STATUS_ENV} \
    POETRY_VERSION=1.1.12 \
    POETRY_HOME="/usr/local"

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

RUN groupadd -r web && useradd -d /code -r -g web web \
    && chown web:web -R /code

WORKDIR $WEBAPP_DIR

COPY --chown=web:web ./pyproject.toml ./poetry.lock $WEBAPP_DIR/

RUN curl -sSL 'https://install.python-poetry.org' | python3 - \
    && poetry --version \
    && poetry config virtualenvs.create false \
    && poetry install --no-root $(if [ "$STATUS_ENV" = 'production' ]; then echo '--no-dev'; fi) --no-interaction --no-ansi \
    && poetry cache clear --all

# Etapa final
FROM python:3.10.12-slim AS production

ENV WEBAPP_DIR=/code/app

WORKDIR $WEBAPP_DIR

# Variables de entorno
ENV STATUS_ENV=${STATUS_ENV}

# Copiar solo los archivos necesarios desde la etapa de construcción
COPY --from=development_build /code /code

# Cambiar al usuario no privilegiado
USER web

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000",