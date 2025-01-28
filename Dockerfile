FROM apache/airflow:2.9.1-python3.9

USER root

# Create airflow group and set permissions
RUN groupadd -g 50000 airflow && \
    usermod -a -G airflow airflow && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq-dev \
        curl \
        unzip \
        git \
    && apt-get clean && \
    apt-get install -y awscli && \
    rm -rf /var/lib/apt/lists/*

# Create directories with numeric permissions
RUN mkdir -p /opt/airflow/datalake/{logs,data} && \
    chown -R 50000:50000 /opt/airflow/datalake

USER airflow

# Environment setup
ENV PYTHONPATH=${PYTHONPATH}:/opt/airflow/dags/scripts \
    AIRFLOW_HOME=/opt/airflow \
    AIRFLOW__CORE__LOAD_EXAMPLES=false

# Dependency installation
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt