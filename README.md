# 📦 ScanStock Deploy

**ScanStock** is a premium inventory and barcode scanning platform designed for high-efficiency warehouse and factory operations.

This repository provides the **official deployment resources** for running ScanStock using Docker containers.

It includes:

* Deployment documentation
* Docker Compose configuration
* Environment configuration template
* Example integration components

> Note: This repository does **not contain the proprietary ScanStock application source code**. It contains the deployment templates required to run the platform. 

---

# 🚀 Quick Start (Docker Compose)

The fastest and recommended way to run **ScanStock** is with **Docker Compose**.

---

# 0️⃣ Pull Docker Image

Before starting, you must pull the **ScanStock** image from your preferred container registry.

## <!-- Option A:  --> GitHub Container Registry (Recommended)

```bash
docker pull ghcr.io/jcp-vision/scanstock:latest
```

[![GitHub Registry](https://img.shields.io/badge/GitHub%20Registry-ghcr.io-blue?style=flat&logo=github)](https://github.com/JCP-VISION/SCANSTOCK/pkgs/container/scanstock)

<!--
## Option B: Docker Hub

```bash
docker pull docker.io/jcpvision/scanstock:latest
```

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-docker.io-blue?style=flat&logo=docker)](https://hub.docker.com/r/jcpvision/scanstock)
-->
---

# 1️⃣ Create Environment File

Copy the example configuration file and create your runtime environment file.

```bash
cp .env.example .env
```

Then edit `.env` and configure the required values:

```ini
LICENSE_KEY=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```

These credentials will be used to initialize the ScanStock administrator account.

---

# 2️⃣ Create `docker-compose.yml`

Create a file called:

```yaml
docker-compose.yml
```

Example configuration:

```yaml
services:

  scanstock:
    image: ghcr.io/jcp-vision/scanstock:latest
    container_name: scanstock
    restart: unless-stopped

    ports:
      - "8000:8000"

    env_file:
      - .env

    volumes:
      - scanstock_data:/var/lib/jcp-vision

volumes:
  scanstock_data:
```

---

# 3️⃣ Start ScanStock

Run:

```bash
docker compose up -d
```

Docker will:

* Pull the ScanStock container
* Create the persistent storage volume
* Start the application

---

# 4️⃣ Access the Application

Open your browser:

```text
http://localhost:8000
```

Login using the administrator credentials defined in your `.env` file.

---

# ⚙ Configuration

ScanStock can be configured using **environment variables inside `.env`**.

The `.env` file is automatically loaded into the container via Docker Compose.

This allows system administrators to customize deployment behavior **without modifying the container image**.

---

# 🧾 Environment Variables Reference

Below is the complete list of supported environment variables that may be configured in the `.env` file.

---

# 🔑 Core Application Settings

These values are **required for initial setup**.

| Variable                  | Description                                         |
| ------------------------- | --------------------------------------------------- |
| LICENSE_KEY               | Your ScanStock license key issued by JCP-VISION     |
| DJANGO_SUPERUSER_USERNAME | Administrator username created during first startup |
| DJANGO_SUPERUSER_PASSWORD | Administrator password                              |
| DJANGO_SUPERUSER_EMAIL    | Administrator email address                         |

These variables are used during the **first initialization of the container** to automatically create the admin account.

Example:

```ini
LICENSE_KEY=XXXX-XXXX-XXXX
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=StrongPassword123
DJANGO_SUPERUSER_EMAIL=admin@company.com
```

---
<!-- 
# 🌐 Application Behavior

These settings control general runtime behavior.

| Variable      | Description                             | Default |
| ------------- | --------------------------------------- | ------- |
| DEBUG         | Enables Django debug mode               | False   |
| ALLOWED_HOSTS | Comma separated list of allowed domains | *       |
| PORT          | Application listening port              | 8000    |

Example:

```
DEBUG=False
ALLOWED_HOSTS=localhost,inventory.company.com
PORT=8000
```

For production deployments **DEBUG must remain disabled**.

---

-->
# 🗄 Database Configuration

By default ScanStock uses **SQLite**, stored inside the persistent Docker volume.

However enterprise deployments can connect to **external databases**.

Enable external database configuration:

```ini
CUSTOM_ENGINE=true
```

Then configure database settings:

| Variable    | Description             |
| ----------- | ----------------------- |
| DB_ENGINE   | Django database backend |
| DB_NAME     | Database name           |
| DB_USER     | Database username       |
| DB_PASSWORD | Database password       |
| DB_HOST     | Database host           |
| DB_PORT     | Database port           |

Example MySQL configuration:

```ini
CUSTOM_ENGINE=true
DB_ENGINE=django.db.backends.mysql
DB_NAME=scanstock
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=mysql
DB_PORT=3306
```

Example PostgreSQL configuration:

```
CUSTOM_ENGINE=true
DB_ENGINE=django.db.backends.postgresql
DB_NAME=scanstock
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=postgres
DB_PORT=5432
```

If `CUSTOM_ENGINE` is not enabled, ScanStock will automatically use the built-in SQLite database.

---

# 📂 Storage Configuration

ScanStock stores runtime data in:

```
/var/lib/jcp-vision
```

This directory contains:

* SQLite database (if used)
<!-- * Uploaded files -->
<!-- * Inventory data -->
* License state
* Runtime application files

Docker mounts this directory as a **persistent volume** so data survives container updates.

---

# 🔐 Security Settings

Optional environment variables may be used for security hardening.

| Variable              | Description                   |
| --------------------- | ----------------------------- |
| SECRET_KEY            | Django secret key override    |
| SESSION_COOKIE_SECURE | Enforce HTTPS session cookies |
| CSRF_COOKIE_SECURE    | Secure CSRF cookies           |

Example:

```ini
SECRET_KEY=super-secret-key
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

These should be configured when deploying behind HTTPS.

---

# 🖨 Printer Integration (Optional)

Factories may integrate **label printers** or barcode printers.

Optional configuration:

| Variable     | Description     |
| ------------ | --------------- |
| PRINTER_MODE | local / network |
| PRINTER_HOST | Printer IP      |
| PRINTER_PORT | Printer port    |

Example:

```ini
PRINTER_MODE=network
PRINTER_HOST=192.168.1.45
PRINTER_PORT=9100
```

This allows direct printing from ScanStock to warehouse label printers.

---

# 💾 Persistent Storage

ScanStock stores runtime data in the mounted Docker volume:

```
/var/lib/jcp-vision
```

This ensures:

* Database persistence
* Uploaded files retained
* License data preserved
* Safe upgrades

---

# 🔧 Maintenance

## View Logs

```bash
docker compose logs -f scanstock
```

## Restart Service

```
docker compose restart
```

## Stop Containers

```
docker compose down
```

---

# 🔄 Updating ScanStock

To upgrade to a newer container version:

```bash
docker compose pull
docker compose up -d
```

Your data will remain intact inside the persistent volume.

---

# 🔐 License

This repository is distributed under the **JCP-VISION Source-Available License**.

This repository may be used to **deploy and operate ScanStock**, but redistribution, resale, or use as part of a competing service is prohibited.

A valid **ScanStock license key** is required to operate the platform.

For licensing inquiries [contact](mailto:licensing@jcp-vision.com):

```text
licensing@jcp-vision.com
```

---

© 2026 **JCP-VISION LIMITED**