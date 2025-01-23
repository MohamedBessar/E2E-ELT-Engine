FROM apache/airflow:2.9.1-python3.9

USER root

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create groups and users before switching to airflow user
RUN groupadd -g 1000 airflow && \
    usermod -g airflow airflow && \
    addgroup --system mygroup && \
    adduser --system --ingroup mygroup myuser

# Switch to the airflow user
USER airflow

# Upgrade pip
RUN pip install --upgrade pip

# Create necessary directories and set permissions
RUN mkdir -p /opt/airflow/datalake/logs && \
    chown -R airflow /opt/airflow/datalake

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/opt/airflow/dags/scripts

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
