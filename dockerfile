FROM apache/airflow:2.10.5rc1-python3.9

USER root
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    wget https://github.com/wal-g/wal-g/releases/download/v1.1/wal-g.linux-amd64.tar.gz && \
    tar -xvf wal-g.linux-amd64.tar.gz && \
    mv wal-g /usr/local/bin/wal-g && \
    rm wal-g.linux-amd64.tar.gz

# Install Python dependencies
RUN pip install psycopg2-binary

# Set Airflow user back
USER airflow
