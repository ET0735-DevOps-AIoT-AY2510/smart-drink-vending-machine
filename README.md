# Smart Drink Vending Machine – IoT-Enabled Vending System

A smart drink vending machine system that supports drink selection, payment flow, barcode redemption, automated stock tracking, environmental monitoring, security alerts, and an admin dashboard for system monitoring and control.

The project connects customer purchase actions, inventory updates, fault detection, admin controls, and operational alerts into one simulated vending machine workflow.

## System Overview

The system simulates a smart vending machine with both customer-facing and admin-facing workflows.

Key capabilities include:

- Drink selection and purchase flow.
- Card and QR code payment support.
- Barcode redemption for online purchases.
- Automated stock tracking and low-stock alerts.
- Dispensing issue detection and inventory discrepancy handling.
- Temperature, leakage, and environmental monitoring.
- Security alerts for door access and burglar detection.
- Admin dashboard for monitoring vending machine status.
- Docker-based setup and testing workflow.

## Features

### Main Menu and Payment

- Displays a welcome screen on startup.
- Allows users to select a drink by entering the drink number and confirming with `#`.
- Validates drink availability before continuing with the purchase flow.
- Supports barcode scanning when `#` is pressed without entering a drink number.
- Supports card payment and QR code payment.
- Allows users to cancel and return to the home screen by pressing `*`.
- Returns to the home screen after 15 seconds of inactivity.

### Barcode Redemption

- Allows users to redeem drinks purchased online using a barcode.
- Supports barcode-based validation before dispensing.
- Prevents redemption when the machine is out of order.

### Dispensing and Stock Management

- Dispenses the selected drink after successful payment or redemption.
- Updates internal inventory after dispensing.
- Uses stock verification to detect possible inventory discrepancies.
- Sends alerts for jams, unexpected dispenses, or stock below 5 units.

### Environmental and Safety Monitoring

- Sends temperature alerts when temperature rises above 10°C.
- Sets the machine to out-of-order at 20°C.
- Detects liquid leakage and places the machine into an out-of-order state.
- Allows ongoing transactions to complete before entering an out-of-order state where appropriate.

### Security and Maintenance

- Supports admin passcode access.
- Allows authorised admin access to disable alarms and unlock the machine door.
- Reactivates the alarm when the door is closed.
- Triggers a buzzer alert if the door remains open for 3–20 minutes.
- Allows the door-open alert duration to be adjusted by admin users.
- Supports burglar/security event detection through sensor-based monitoring.

### User and Admin Web API

- Supports user account management.
- Allows users to view the drink menu.
- Allows online purchases that generate redeemable codes/barcodes.
- Provides an admin dashboard for monitoring and adjusting stock.
- Allows admins to view temporary passcodes and manage alert emails.

### Database

The database supports:

- Admin credentials.
- User credentials.
- Reserved stock for paid but uncollected drinks.
- Physical stock records for drink inventory inside the machine.

## Key Operational Rules

| Rule | Threshold / Behaviour |
|---|---|
| Inactivity timeout | 15 seconds |
| Low-stock alert | Below 5 units |
| Temperature warning | Above 10°C |
| Out-of-order temperature | 20°C |
| Door-open alert window | 3–20 minutes |
| Testing workflow | PyTest |
| Deployment/testing setup | Docker |

## Repository Structure

```text
docs/                    Project documentation and supporting files
src/                     Main source code for vending machine logic and web/API features
Dockerfile               Docker image configuration
docker-compose.yml       Docker Compose setup
requirements.txt         Python dependencies
README.md                Project overview and setup guide
```

## Technical Stack

- Python
- HTML / CSS
- Docker
- Docker Compose
- PyTest
- Database-backed application logic
- Admin dashboard
- Barcode redemption workflow
- Payment flow simulation
- Environmental monitoring logic
- Security and maintenance alert logic

## Running with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/ET0735-DevOps-AIoT-AY2510/smart-drink-vending-machine.git
cd smart-drink-vending-machine
```

### 2. Build the Docker Image

```bash
docker compose build
```

### 3. Run the Interactive Docker Shell

```bash
docker run -it \
  --privileged \
  --device=/dev/* \
  -v /run/udev:/run/udev:ro \
  -p 5000:5000 \
  smart-drink-vending-machine-vending-machine sh
```

> Note: If the Docker image name differs on your machine, run `docker images` and replace `smart-drink-vending-machine-vending-machine` with the correct image name.

## Once Inside the Docker Shell

### 1. Initialise the Database

```bash
python3 database_setup.py
```

### 2. Run the Main Python Script in the Background

```bash
python3 F123456789.py &
```

### 3. Change the Mock Temperature for Testing

```bash
python3 settemp.py <value>
```

Example:

```bash
python3 settemp.py 12
```

## Running Tests

Run the PyTest test suite:

```bash
pytest
```

If tests are stored in a specific folder, run:

```bash
pytest tests/
```

## Demo Video

Demo folder: [Google Drive Demo Video](https://drive.google.com/drive/folders/1g4HWi8hh0Cg1HQ0AUzOtiVWKkkE3ZSNq)

## Team Contributions

### Nathan

Responsible for F1, F4, F5, and F9.

Contributions included:

- PyTests for F1, F2, F4, F5, F7, and F9.
- SRS documentation and flowcharts.
- Integration of F1, F4, and F5.
- Preparation of Excel sheets for PyTest results and physical test cases.

GitHub: `FootOfTheFoot`

### Terence

Responsible for F3, F6, and F8.

Contributions included:

- PyTests for F3, F6, and F8.
- SRS documentation and flowcharts.
- Integration of remaining functionalities.
- Containerisation files.
- Database setup.
- Admin dashboard.

GitHub: `T3rrybl3`

### Mark

Responsible for F7 and SRS flowcharts.

GitHub: `bununu2`

### Zayan

Responsible for F2, user API design, and SRS flowcharts.

GitHub: `zayanfm`

## What This Project Demonstrates

This project demonstrates how a vending machine workflow can be modelled as an integrated software system. Payment flow, barcode redemption, stock tracking, environmental monitoring, security alerts, admin controls, testing, and deployment setup all need to work together for the system to behave reliably.

It also highlights the importance of operational rules and edge-case handling, such as timeout behaviour, low-stock thresholds, temperature limits, leakage detection, door-open alerts, and out-of-order handling.
