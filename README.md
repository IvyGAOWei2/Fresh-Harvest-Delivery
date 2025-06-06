# COMP639S1_Project_2_Group_AZ

# FreshHarvestDelivery Guide

An online shopping platform for fresh produce, built with Flask & MySQL (Backend) and HTML/CSS/JS (Frontend). Developed within an Agile team.

## ⚙️ Features

- Customer & Admin login
- Product management (CRUD)
- Cart & order history
- Gift card support
- Admin dashboard

---

## 📸 Project Demo – User Interface Walkthrough

The following demo videos showcase the core features of the **FreshHarvestDelivery** platform, including both customer and admin workflows.

🛒 Customer View:

🧑‍💼 Admin View:

### 🎯 Features Demonstrated

**Customer Workflow**

- Browse products and view details
- Add to cart and adjust quantities
- Complete checkout and view order history

**Admin Workflow**

- Admin login and dashboard
- Add/edit/delete product information
- Manage orders and customer data
- Gift card creation and redemption

---

## Initialize project

_(Only needs to be run once)_

### Mac or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip3 install -r requirements.txt
```

## Run Project

### Mac or Linux

```bash
./run.sh
```

### Windows

```bash
run.cmd
```

## Database Connection

### Local Database File

The db file for the database is located at `dbFile/freshHarvestDelivery.sql`

### Configuration File

The configuration file for the database connection is located at `dbFile/config_example`, please copy this file and rename it to `dbFile/config.cnf`, then configure with your own

### Database Load

run freshHarvestDelivery.sql then dataImport.sql

### Configuration Example

```ini
[client]
user = your_username
password = your_password
host = localhost
port = 3306
database = your_db_name
```
