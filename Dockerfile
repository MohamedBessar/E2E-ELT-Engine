FROM apache/airflow:2.9.1-python3.9

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directory structure with proper ownership
# Use numeric UID/GID from base image (airflow user is 50000:50000)
RUN mkdir -p /opt/airflow/datalake/logs && \
    chown -R 50000:50000 /opt/airflow/datalake

USER airflow

# Environment configuration
ENV PYTHONPATH=/opt/airflow/dags/scripts \
    AIRFLOW_HOME=/opt/airflow \
    AIRFLOW__CORE__LOAD_EXAMPLES=false

# Upgrade pip and install requirements
COPY --chown=50000:50000 requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt