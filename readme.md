# FastAPI MongoDB Template

Este es un repositorio de plantilla que te permite comenzar rápidamente con la creación de una aplicación web usando FastAPI y MongoDB. ya sea con docker o con un entorno virtual con pyenv y poetry

## Características

- Configuración básica de una aplicación FastAPI con MongoDB.
- Ejemplos de rutas y modelos para comenzar a construir tu API.
- Integración con Docker para un entorno de desarrollo aislado.
- Ejemplos de cómo realizar operaciones básicas con la base de datos MongoDB.

## Requisitos previos

- Docker y Docker Compose instalados en tu máquina. Preferiblemente con [docker desktop](https://www.docker.com/products/docker-desktop/)
- [pyenv](https://github.com/pyenv/pyenv#installation) o [pyenv-win](https://github.com/pyenv-win/pyenv-win#quick-start)
- [poetry](https://python-poetry.org/docs/#installation)


## Pasos iniciales

* Clona este repositorio:

```bash
git clone https://github.com/EdwarMontano/template_fastAPI_mongodb.git
cd template_fastAPI_mongodb
```
* Crea un archivo .env en la raíz del proyecto con las siguientes variables:

```text
ENVIRONMENT=
DEBUG=
STATUS_ENV=

MONGO_HOST=
MONGO_PORT=27017
MONGO_USER=
MONGO_PASS=
MONGO_DB=
MONGO_COLLECTION=
MONGO_TEST_DB=

MONGO_URL=
MONGO_URL_test=
```

## Instalación con Docker
es el modo fácil de levantar el proyecto
```bash
docker compose --profile web  build
docker compose --profile web  up
```
## Instalación con pyenv y poetry
es el modo difícil  de levantar el proyecto  pero nos sirve para habilitar las opciones de debug mas fácil. recuerde instalar un motor de mongo para la bd.
```bash
pyenv versions #opcional: sirve para comprobar si la version de python que necesitamos ya se encuentra descargada
pyenv install --list #opcional: sirve para listar los versiones disponible por pyenv
pyenv install 3.10.12 
```

```bash
poetry --version
poetry env info
poetry env use $(pyenv which python)
poetry env info # la version de python debe coincidir 
poetry shell 
poetry install
poetry show # dependencias instaladas == pip list
poetry add [dependecias]
```
🚫 :sos: Si al realizar la instalación de las dependencia se presenta un error. Elimanar el archivo poetry.lock y ejecutar el siguiente comando

```bash
poetry lock --no-update
```

finalmente correr el server con:

```bash
uvicorn app.main:app --reload 
```
generar requirements:

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt 
```
