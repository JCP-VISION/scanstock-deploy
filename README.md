# 📦 ScanStock Deployment Guide

ScanStock is a **warehouse inventory and barcode scanning platform** designed for manufacturing plants, warehouses, and industrial operations.

This repository provides the **official deployment configuration** for running ScanStock using Docker containers.

It includes:

* Deployment documentation
* Environment configuration template
* Docker Compose configuration
* Runtime configuration reference

> **Important**
> This repository does **not include the proprietary ScanStock application source code**.
> It provides the deployment configuration required to run the ScanStock container.

---

# 🚀 Deployment Overview

ScanStock runs as a **Docker container**.

Administrators configure the system using:

1️⃣ Environment variables (`.env`)
2️⃣ Docker Compose configuration
3️⃣ Persistent storage volumes

The container includes everything required to run the application.

---

# 🐳 Step 1 — Pull the ScanStock Image

## <!-- Option A: --> GitHub Container Registry (Recommended)

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

# ⚙ Step 2 — Create Environment Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Edit `.env` and configure the required variables.

Minimum required configuration:

```ini
LICENSE_KEY=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```

These values are used **during the first container startup** to automatically create the administrator account.

Example:

```ini
LICENSE_KEY=XXXX-XXXX-XXXX
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=StrongPassword123
DJANGO_SUPERUSER_EMAIL=admin@company.com
```

---

# 🧱 Step 3 — Create `docker-compose.yml`

Create a file called:

```
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

# 🔌 Port Configuration

ScanStock runs **inside the container on port 8000**.

You may map this to any port on your server.

Example:

```yaml
ports:
  - "8080:8000"
```

This means:

```
Host Port → 8080
Container Port → 8000
```

Access the application at:

```
http://server-ip:8080
```

---

# ▶ Step 4 — Start the Application

Run:

```bash
docker compose up -d
```

Docker will:

* Start the ScanStock container
* Initialize the application
* Create the administrator account
* Prepare database and static assets

---

# 🔧 Container Initialization

On the **first startup**, the ScanStock container automatically performs:

1️⃣ Database migrations
2️⃣ Administrator account creation
3️⃣ Static asset collection
4️⃣ Runtime storage initialization

No manual setup steps are required.

These tasks are handled automatically by the container entrypoint.

---

# 🌐 Step 5 — Access ScanStock

Open the application in your browser.

Example:

```
http://server-ip:HOST_PORT
```

Example if using port mapping `8080:8000`:

```
http://localhost:8080
```

Login using the administrator credentials defined in `.env`.

---

# ⚙ Runtime Configuration

ScanStock can be configured using environment variables inside `.env`.

Configuration priority:

```
Environment Variables (.env)
        ↓
pyproject.toml defaults
        ↓
Application fallback defaults
```

This allows administrators to **override application behavior without modifying the container image**.

---

# 🔑 Core Variables

These variables are required for initial setup.

| Variable                  | Description            |
| ------------------------- | ---------------------- |
| LICENSE_KEY               | ScanStock license key  |
| DJANGO_SUPERUSER_USERNAME | Administrator username |
| DJANGO_SUPERUSER_PASSWORD | Administrator password |
| DJANGO_SUPERUSER_EMAIL    | Administrator email    |

---

# 🌐 Application Settings

| Variable      | Description                | Default        |
| ------------- | -------------------------- | -------------- |
| DEBUG         | Enable Django debug mode   | False          |
| ALLOWED_HOSTS | Allowed domains            | *              |
| SECRET_KEY    | Override Django secret key | auto-generated |

Example:

```ini
DEBUG=False
ALLOWED_HOSTS=localhost,inventory.company.com
SECRET_KEY=your-secret-key
```

For production deployments **DEBUG must remain disabled**.

---

# 🔐 Security Settings

Optional security settings:

| Variable              | Description                       |
| --------------------- | --------------------------------- |
| SESSION_COOKIE_SECURE | Require HTTPS for session cookies |
| CSRF_COOKIE_SECURE    | Require HTTPS for CSRF cookies    |

Example:

```ini
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

These should be enabled when deploying behind **HTTPS or a reverse proxy**.

---

# 🖨 ScanStock Operational Settings

These control **system behavior and scanning features**.

| Variable                    | Description                          | Default |
| --------------------------- | ------------------------------------ | ------- |
| WEB_LABEL_PRINTER           | Enable web label printing            | True    |
| TRANSACTION_APPROVAL_NEEDED | Require approval for transactions    | True    |
| LOGIN_AUTH_NEEDED           | Require authentication barcode login | True    |
| ALLOW_ORDER_ENTRY           | Allow manual order entry             | True    |
| LOGIN_BARCODE_OVERRIDE      | Allow barcode login override         | False   |

Example:

```ini
WEB_LABEL_PRINTER=True
TRANSACTION_APPROVAL_NEEDED=True
LOGIN_AUTH_NEEDED=True
ALLOW_ORDER_ENTRY=True
LOGIN_BARCODE_OVERRIDE=False
```

---

# 📦 Barcode Scanning Configuration

These settings define **barcode formats recognized by the system**.

| Variable         | Description                               |
| ---------------- | ----------------------------------------- |
| ITEM_SCAN_REGEX  | Regex pattern for item barcodes           |
| QTY_SCAN_REGEX   | Regex pattern for quantity scans          |
| AUTH_SCAN_REGEX  | Regex pattern for authentication barcodes |
| ORDER_SCAN_REGEX | Regex pattern for order barcodes          |

Example:

```ini
ITEM_SCAN_REGEX=/^SS-\d{6}-JCV$/
QTY_SCAN_REGEX=/^QTY:[A-Za-z0-9]+\|UNIT:[A-Za-z0-9]+$/
AUTH_SCAN_REGEX=/^(USR|USER):[^|]+\|(PWD|PASSWORD):[^|]+\|AUTH:JCV$/
ORDER_SCAN_REGEX=/^MOS-\d+$/
```

---

# 🔁 License & System Checks

These settings control licensing validation.

| Variable                       | Description                   | Default |
| ------------------------------ | ----------------------------- | ------- |
| CHECK_PERIODIC                 | Enable periodic system checks | True    |
| LICENSE_CHECK_INTERVAL_SECONDS | License validation interval   | 300     |

Example:

```ini
CHECK_PERIODIC=True
LICENSE_CHECK_INTERVAL_SECONDS=300
```

---

# 🖨 Printer Configuration

Configure the internal label printing service.

| Variable           | Description                            | Default |
| ------------------ | -------------------------------------- | ------- |
| PRINTER_LOCAL_PORT | Port used by the local printer service | 54321   |

Example:

```ini
PRINTER_LOCAL_PORT=54321
```

---

# 🗄 Database Configuration

By default ScanStock uses **SQLite stored in the persistent Docker volume**.

Enterprise deployments may connect to an external database.

Enable external database support:

```ini
CUSTOM_ENGINE=true
```

Then configure the database connection.

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
DB_PASSWORD=password
DB_HOST=mysql
DB_PORT=3306
```

Example PostgreSQL configuration:

```ini
CUSTOM_ENGINE=true
DB_ENGINE=django.db.backends.postgresql
DB_NAME=scanstock
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=postgres
DB_PORT=5432
```

---

# 💾 Persistent Storage

ScanStock stores runtime data inside:

```
/var/lib/jcp-vision
```

This directory contains:

* SQLite database (if used)
* license data
* uploaded media
* runtime system data

The directory **must be mounted as a Docker volume**.

Example:

```yaml
volumes:
  - scanstock_data:/var/lib/jcp-vision
```

This ensures data persists between container updates.

---

# 📄 Logs

View container logs:

```bash
docker compose logs -f scanstock
```

---

# 🔄 Updating ScanStock

To update the container:

```bash
docker compose pull
docker compose up -d
```

Because runtime data is stored in the Docker volume, your data will remain intact.

---

# 🔄 Updating Environment Configuration

After modifying `.env`, restart the container:

```bash
docker compose down
docker compose up -d
```

---

# 🔐 Licensing

ScanStock requires a valid license key.

For licensing inquiries:

```
licensing@jcp-vision.com
```

---

© 2026 **JCP-VISION LIMITED**