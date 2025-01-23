FROM apache/airflow:2.9.1-python3.9

USER root

<<<<<<< HEAD
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
=======

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN groupadd -g 1000 airflow && \
    usermod -g airflow airflow && \
    addgroup --system mygroup && \
    adduser --system --ingroup mygroup myuser

USER airflow


RUN pip install --upgrade pip


RUN mkdir -p /opt/airflow/datalake/logs && \
    chown -R airflow /opt/airflow/datalake


ENV PYTHONPATH=/opt/airflow/dags/scripts


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
>>>>>>> 330ddfd (update docekr-compose)
