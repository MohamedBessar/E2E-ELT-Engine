FROM apache/airflow:2.10.4-python3.12

# Switch to root user for installing packages
USER root

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Upgrade pip
RUN pip install --upgrade pip

# Create directories for logs and set permissions
RUN mkdir -p /opt/airflow/incloud/datalake/logs && \
    chown -R airflow /opt/airflow/incloud/datalake


# Set PYTHONPATH for accessing custom scripts
ENV PYTHONPATH=/opt/airflow/dags/scripts

# Copy requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and scripts into the container
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

RUN airflow db migrate
# Set entrypoint for Airflow (if needed)
# ENTRYPOINT ["/usr/local/bin/airflow"]