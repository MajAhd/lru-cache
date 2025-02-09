from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import psycopg2
import logging
import os

# Database credentials (use Airflow Variables or Env Vars for production)
SOURCE_DB = {
    "host": "source_host",
    "port": "5432",
    "database": "source_db",
    "user": "source_user",
    "password": "source_password"
}

DEST_DB = {
    "host": "dest_host",
    "port": "5432",
    "database": "dest_db",
    "user": "dest_user",
    "password": "dest_password"
}

BACKUP_DIR = "/dbBackup"
WAL_G_BINARY = "/usr/local/bin/wal-g"

logging.basicConfig(level=logging.INFO)


def check_db_connection(db_config):
    try:
        conn = psycopg2.connect(**db_config)
        conn.close()
        logging.info(f"Connected to {db_config['database']} successfully.")
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        raise


def backup_database():
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        cmd = f"WALG_FILE_PREFIX={BACKUP_DIR} {WAL_G_BINARY} backup-push /var/lib/postgresql/data"
        subprocess.run(cmd, shell=True, check=True)
        logging.info("Backup completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup failed: {str(e)}")
        raise


def restore_database():
    try:
        cmd = f"WALG_FILE_PREFIX={BACKUP_DIR} {WAL_G_BINARY} backup-fetch /var/lib/postgresql/data LATEST"
        subprocess.run(cmd, shell=True, check=True)
        logging.info("Restore completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Restore failed: {str(e)}")
        raise


# Define DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        'postgres_backup_restore',
        default_args=default_args,
        description='Backup and Restore PostgreSQL Databases',
        schedule_interval=None,
        start_date=datetime(2023, 1, 1),
        catchup=False,
) as dag:
    connect_source = PythonOperator(
        task_id='connect_source_db',
        python_callable=check_db_connection,
        op_kwargs={'db_config': SOURCE_DB}
    )

    backup_task = PythonOperator(
        task_id='backup_database',
        python_callable=backup_database
    )

    connect_dest = PythonOperator(
        task_id='connect_dest_db',
        python_callable=check_db_connection,
        op_kwargs={'db_config': DEST_DB},
        retries=5,
        retry_delay=timedelta(minutes=1)
    )

    restore_task = PythonOperator(
        task_id='restore_database',
        python_callable=restore_database,
        retries=3,
        retry_delay=timedelta(minutes=5)
    )

# Define task dependencies
connect_source >> backup_task >> connect_dest >> restore_task
