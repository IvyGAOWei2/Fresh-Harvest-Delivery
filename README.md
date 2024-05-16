# COMP639S1_Project_2_Group_AZ

# FreshHarvestDelivery Guide

## Website demo

[Under construction](https://github.com/LUMasterOfAppliedComputing2024S1/COMP639S1_Group_AZ)

## Project Milestone
Sprint1 published on 15/05/2024


## Initialize project
*(Only needs to be run once)*

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
The configuration file for the database connection is located at `dbFile/config_example`, please configure this file and rename it to `dbFile/config.cnf`


### Configuration Example
```ini
[client]
user = your_username
password = your_password
host = localhost
port = 3306
database = your_db_name
```