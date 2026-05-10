# Zara Clinic - Hospital Management System (Software Re-Engineering Project)

## Overview

**Zara Clinic** is a comprehensive Hospital Management System developed using Java Swing for the graphical user interface and MySQL for database management.

This project was further enhanced as part of a **Software Re-Engineering Project**, where the legacy application was analyzed, refactored, and improved using modern software engineering practices.

The repository includes:

- Legacy Java Swing Hospital Management System
- SonarQube static code analysis configuration
- Refactored MySQL database schema
- Prisma ORM schema design
- Python ETL migration script for data cleansing and migration
- Database refactoring scripts

The system focuses on managing hospital operations such as patient management, doctor management, secure admin login, and real-time database operations.

---

# Features

## Legacy Application Features

### Admin Login
- Secure login system for administrators only.
- Authentication-based access to hospital management modules.

### CRUD Operations

#### Patient Management
- Add new patients
- View patient records
- Update patient information
- Delete patient records

#### Doctor Management
- Add new doctors
- View doctor records
- Update doctor information
- Delete doctor records

### Real-Time Database Connectivity
- All records are stored and retrieved from MySQL database in real time.

### Logout System
- Secure logout option that redirects users back to the login page.

---

# Software Re-Engineering Components

## 1. Static Code Analysis using SonarQube
The project integrates SonarQube for:

- Detecting code smells
- Identifying duplicated code
- Measuring technical debt
- Improving maintainability
- Enhancing software quality

## 2. Database Refactoring
The original database schema was refactored to remove multiple data smells such as:

- Overloaded columns
- Duplicate data
- Non-atomic fields
- Derived data redundancy

The new database structure follows normalization principles and improved schema design.

## 3. Prisma ORM Schema
The repository includes a Prisma schema file (`schema.prisma`) for modern ORM-based database modeling and management.

## 4. ETL Data Migration
A Python ETL migration script (`migration_etl.py`) was developed to:

- Clean legacy appointment data
- Transform invalid legacy formats
- Normalize room data
- Validate appointment status values
- Migrate data into the refactored database schema

### ETL Transformations Implemented

#### T1 - Date Conversion
Legacy string-based dates are converted into proper DATETIME values.

#### T2 - Room Data Splitting
Overloaded room columns are separated into:
- room_number
- building_block

#### T3 - Duplicate Data Removal
Redundant patient and doctor information is removed from appointment records.

#### T4 - Status Validation
Only valid appointment status codes are allowed:
- P = Pending
- C = Completed
- X = Cancelled
- H = Hold
- R = Rescheduled

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Java Swing | GUI Development |
| Java | Backend Application Logic |
| MySQL | Database Management |
| Prisma ORM | Refactored Database Modeling |
| Python 3 | ETL Data Migration |
| SonarQube | Static Code Analysis |
| Maven | Build & Dependency Management |
| Docker | SonarQube Containerization |

---

# Project Structure

```bash
Zara-Clinic/
│
├── src/                         # Java Swing source files
├── Database/
│   ├── database_refactoring.sql
│   └── legacy_schema.sql
│
├── migration_etl.py             # Python ETL migration script
├── schema.prisma                # Prisma ORM schema
├── sonar-project.properties     # SonarQube configuration
├── pom.xml                      # Maven configuration
├── Screenshots/
│   ├── login.PNG
│   ├── welcome.PNG
│   ├── patient.PNG
│   └── doctor.PNG
│
└── README.md
```

---

# Complete Setup and Execution Guide

## Prerequisites

Before running the project, install the following:

- Java JDK 8 or later
- NetBeans / IntelliJ IDEA / Eclipse
- MySQL Server
- MySQL Workbench
- Python 3
- Maven
- Docker Desktop
- SonarQube

---

# Step 1 - Clone Repository

```bash
git clone <repository-url>
cd Zara-Clinic
```

---

# Step 2 - Configure MySQL Database

## Create Database

Open MySQL Workbench or MySQL terminal and create the database:

```sql
CREATE DATABASE hospital_legacy;
```

---

# Step 3 - Load Refactored Database Schema

Execute the SQL refactoring script:

```bash
mysql -u root -p hospital_legacy < Database/database_refactoring.sql
```

This will:

- Create refactored tables
- Normalize database structure
- Remove legacy data smells

---

# Step 4 - Configure Database Credentials

Update your MySQL credentials inside:

- `migration_etl.py`
- Java database connection files/classes

Example:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'hospital_legacy'
}
```

---

# Step 5 - Install Python Dependency

Install MySQL connector for Python:

```bash
pip install mysql-connector-python
```

---

# Step 6 - Run ETL Migration Script

Run the migration script:

```bash
python migration_etl.py
```

The ETL script performs:

- Data cleansing
- Date transformation
- Room normalization
- Validation checks
- Migration into refactored schema

---

# Step 7 - Start SonarQube using Docker

Ensure Docker Desktop is running.

Run SonarQube container:

```bash
docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
```

SonarQube will be available at:

```text
http://localhost:9000
```

Default Login:

```text
Username: admin
Password: admin
```

---

# Alternative - Run SonarQube Locally (Windows)

If SonarQube is installed locally:

```powershell
Start-Process -FilePath "C:\sonarqube\bin\windows-x86-64\StartSonar.bat"
```

---

# Step 8 - Run Sonar Scanner using Maven

Execute SonarQube analysis:

```bash
mvn clean verify sonar:sonar -Dsonar.projectKey=HospitalManagementSystem -Dsonar.login=YOUR_SONAR_TOKEN
```

Example:

```bash
mvn clean verify sonar:sonar -Dsonar.projectKey=HospitalManagementSystem -Dsonar.login=sqp_xxxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Step 9 - Run the Java Swing Application

## Using NetBeans / IntelliJ / Eclipse

1. Open the project in your IDE.
2. Build the project.
3. Run the `LoginPage` class.

---

# Application Usage

## Login

- Enter admin credentials.
- Access patient and doctor management modules.

## Manage Patients

Perform:
- Create
- Read
- Update
- Delete

operations for patients.

## Manage Doctors

Perform:
- Create
- Read
- Update
- Delete

operations for doctors.

## Logout

Use the logout button to securely return to the login screen.

---

# Screenshots

## Login Page

![Login Page](https://github.com/zahidrahimoon/Hospital-Management-System/blob/master/Screenshots/login.PNG)

## Welcome Page

![Welcome Page](https://github.com/zahidrahimoon/Hospital-Management-System/blob/master/Screenshots/welcome.PNG)

## Patient Management

![Patient Management](https://github.com/zahidrahimoon/Hospital-Management-System/blob/master/Screenshots/patient.PNG)

## Doctor Management

![Doctor Management](https://github.com/zahidrahimoon/Hospital-Management-System/blob/master/Screenshots/doctor.PNG)

---

# SonarQube Analysis Goals

The software re-engineering process focused on improving:

- Maintainability
- Reliability
- Code readability
- Database normalization
- Technical debt reduction
- Software quality metrics

---

# Future Improvements

Potential future enhancements include:

- Role-based authentication
- Appointment scheduling system
- Billing module
- REST API integration
- Cloud database deployment
- Web-based interface using Spring Boot
- Dockerized full-stack deployment

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for more details.

---

# Contact

For queries or contributions:

- Email: zahidrahimoon22@gmail.com
- LinkedIn: https://www.linkedin.com/in/zahidrahimoon/

