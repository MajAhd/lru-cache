# pg-backup-orchestrator

## Overview
`pg-backup-orchestrator` is an automated **PostgreSQL backup & restore** tool using **Airflow, Python, and WAL-G**. It facilitates seamless database backups and restorations, supporting **small to large databases** while ensuring reliability and error handling.

## Features
-  **Automated Backup & Restore**: Uses **WAL-G** for efficient PostgreSQL backups.
-  **Airflow Orchestration**: Manages the backup workflow with retries and logging.
-  **Dockerized Setup**: Easily deploy using **Docker & Docker Compose**.
-  **Error Handling & Rollback**: Ensures data consistency in case of failures.
-  **Supports External Databases**: Works with databases outside of Docker.

## Tech Stack
- **Python** (for scripting and automation)
- **Apache Airflow** (for workflow orchestration)
- **WAL-G** (for PostgreSQL backup & restore)
- **Docker & Docker Compose** (for deployment)

## Setup & Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/pg-backup-orchestrator.git
cd pg-backup-orchestrator
```

### Apache Airflow

```sh
# initial Airflow
docker-compose up airflow-init
        
# Run Airflow        
docker-compose up
```
open http://localhost:8080

### [More Info to setup Airflow and Docker](https://airflow.apache.org/docs/apache-airflow/2.1.1/start/docker.html) 
### 2️⃣ Create a Docker Network (if needed)
```bash
docker network create external_db_net
```

### 3️⃣ Build and Run the Project
```bash
docker compose up --build
```

### 4️⃣ Access Airflow UI
Open your browser and go to **[http://localhost:8080](http://localhost:8080)**.

## Configuration
Modify the **database credentials** inside `dags/backup_restore.py`:

```python
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
```

For production, store credentials securely using **Airflow Variables or Secrets Manager**.

## Usage
1. **Trigger the DAG manually in Airflow UI** or schedule it.
2. The DAG performs:
   - **Database Connection Check** (Fails if unreachable)
   - **Backup Using WAL-G** (Stored in `dbBackup` directory)
   - **Restore to Target Database** (With rollback on failure)
3. Monitor logs in **Airflow UI**.

## Troubleshooting
- If the DAG fails, check Airflow logs.
- Ensure **PostgreSQL is accessible** from the Airflow container.
- Use `docker logs airflow` for debugging.

## Roadmap & Future Enhancements
✅ Automate retrying failed restores  
✅ Add email notifications for failures  
🚀 Support incremental backups  
🚀 Improve security with **Vault/Secrets Manager**

## License
This project is licensed under the [**MIT License**](./readme.MD)

## Contributors
👤 [**Majid Ahmaditabar**](https://www.linkedin.com/in/majahd/)

Feel free to contribute! Submit a PR or open an issue. 😊

