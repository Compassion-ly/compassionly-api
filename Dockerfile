# Use the official Python 3.10 slim image from Docker Hub
FROM python:3.10-slim

# Set environment variables to ensure Python outputs are sent straight to terminal without being buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Copy .env and serviceAccountKey.json into the container
COPY .env /app/
COPY serviceAccountKey.json /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy poetry.lock* and pyproject.toml in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-dev

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ]; then poetry install --no-root; else poetry install --no-root --only main; fi"

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy other necessary files and directories into the container
COPY ./scripts/ /app/
COPY ./alembic.ini /app/
COPY ./tests-start.sh /app/
COPY ./app /app/app

EXPOSE 80

# run 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Remaining Docker commands for tagging and pushing the image can stay as comments for reference
# docker tag compassionly-api asia-southeast2-docker.pkg.dev/compassion-ly-app/compassionly-api/compassionly-api:1.0
# docker push asia-southeast2-docker.pkg.dev/compassion-ly-app/compassionly-api/compassionly-api:1.0