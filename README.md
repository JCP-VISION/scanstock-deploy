# 📦 ScanStock

**ScanStock** is a premium inventory and barcode scanning platform designed for efficiency and ease of use. This repository contains the source code and container configuration for deploying ScanStock as a robust, scalable service.

---

## 🚀 Quick Start with Docker Compose

The fastest and recommended way to run **ScanStock** is with **Docker Compose**. This allows you to define configuration, networking, and volumes in a single file.

---

## 1️⃣ Create Environment File

Copy the example environment file and update it with your credentials.

```bash
cp .env.example .env
```

> **Important:** At minimum you must set:

```
LICENSE_KEY=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=
```

---

## 2️⃣ Create `docker-compose.yml`

Create the following file in the project directory.

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

## 3️⃣ Start the Application

Run:

```bash
docker compose up -d
```

This will:

* Pull the ScanStock container
* Create the persistent storage volume
* Start the application

---

## 4️⃣ Access the Application

Open your browser:

```
http://localhost:8000
```

Login using the admin credentials defined in your `.env` file.

---

# 🛠️ Configuration

ScanStock can be configured using environment variables in `.env`.

## Core Settings

| Variable                  | Description            |
| ------------------------- | ---------------------- |
| LICENSE_KEY               | Your ScanStock license |
| DJANGO_SUPERUSER_USERNAME | Admin username         |
| DJANGO_SUPERUSER_PASSWORD | Admin password         |
| DJANGO_SUPERUSER_EMAIL    | Admin email            |

---

# 🗄 Database Configuration

By default ScanStock uses **SQLite** stored inside the persistent volume.

If you want to use **MySQL or PostgreSQL**, enable the custom engine.

```
CUSTOM_ENGINE=true
DB_ENGINE=django.db.backends.mysql
DB_NAME=scanstock
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=mysql
DB_PORT=3306
```

---

# 💾 Persistent Storage

ScanStock stores important runtime data in the mounted volume:

```
/var/lib/jcp-vision
```

Contents include:

* SQLite database
* Uploaded media
* License state

This ensures data survives container restarts and updates.

---

# 🔄 Maintenance

## View Logs

```
docker compose logs -f scanstock
```

## Restart

```
docker compose restart
```

## Stop

```
docker compose down
```

---

# 🔄 Updating ScanStock

To upgrade to a new version:

```bash
docker compose pull
docker compose up -d
```

Your data will remain intact in the persistent volume.

---

# 🖥 Platform Support

ScanStock runs in a **Linux-based container**.

For Windows users:

Ensure **Docker Desktop** is running in **Linux container mode**.

---

© 2026 JCP‑VISION LIMITED
