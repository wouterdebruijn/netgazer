# Netgazer
Netgazer is a minimalistic network scanner that discovers devices within a network. It is designed to be used in automated network discovery. It is written in Python and uses nmap to gather initial information about a discovered device, after which a matching device inspection module is used to gather more detailed information about the device.

Gathered information is stored in a SQLite database, managed by Django. The database can be accessed through the REST API and the admin interface.

## Installation
1. Clone the repository
2. Install the required packages
```bash
pip install -r requirements.txt
```

## Usage
1. Start the Django server
```bash
python manage.py runserver
```

2. Start the scanner
```bash
python netgazer_cli.py discover <inital_device_ip>
```

