# CareerHub — Job Portal Web Application

CareerHub is a full-stack job portal web application built using **Python, Flask, SQLite, and Bootstrap 5**. It provides a platform where job seekers can explore job opportunities and apply for positions, while employers can post and manage jobs. Administrators can manage users, job listings, and applications.

🌐 **Live Website:** https://job-portal-project-crnm.onrender.com
💻 **GitHub Repository:** https://github.com/nischith-ctrl/job_portal_project

---

## ✨ Features

### 👤 User Authentication

* User registration and login.
* Password hashing for account security.
* Session management using Flask-Login.
* Role-based access for job seekers, employers, and administrators.

### 🔍 Job Search

* Browse available job listings.
* Search jobs by keyword.
* Filter jobs by location, category, and company.
* View detailed information about individual jobs.

### 📝 Job Applications

* Job seekers can apply for available positions.
* Submit resume links and cover letters.
* Prevent duplicate applications for the same job.
* Track submitted applications through the dashboard.

### 🏢 Employer Dashboard

* Post new job listings.
* Edit existing job listings.
* Delete job listings.
* View applications associated with posted jobs.
* Update application statuses.

### 🛡️ Admin Dashboard

* View registered users.
* View job listings and applications.
* Manage user accounts.
* Manage job listings and application statuses.

### 🌐 API Integration

* Public REST API endpoint: `/api/jobs`
* Import remote job listings using the Remotive API.
* Return job listings in JSON format.

### 🎨 User Interface

* Responsive web interface using Bootstrap 5.
* HTML templates rendered with Flask and Jinja.
* Static assets organized in the `static/` directory.

---

## 🛠️ Technologies Used

| Technology       | Purpose                                 |
| ---------------- | --------------------------------------- |
| Python           | Backend programming                     |
| Flask            | Web application framework               |
| Flask-SQLAlchemy | Database integration and ORM            |
| SQLite           | Database storage                        |
| Flask-Login      | User authentication and sessions        |
| Werkzeug         | Password hashing and security utilities |
| Requests         | External API communication              |
| HTML5            | Web page structure                      |
| CSS3             | Styling                                 |
| Bootstrap 5      | Responsive user interface               |
| Jinja            | Dynamic HTML templates                  |
| Gunicorn         | Production WSGI server                  |
| Render           | Web application deployment              |
| Git and GitHub   | Version control and source code hosting |

---

## 📁 Project Structure

The main files and folders in the repository are organized as follows:

```text
job_portal_project/
│
├── static/              # Static assets such as CSS, JavaScript, and images
│
├── templates/           # HTML templates rendered by Flask
│
├── venv/                # Local Python virtual environment
│
├── app.py               # Main Flask application
│
├── requirements.txt     # Python dependencies
│
├── job_portal.sqlite3   # SQLite database used by the application
│
├── job_portal.db        # Additional database file in the repository
│
└── README.md            # Project documentation
```

**Important:** The application code in `app.py` configures SQLAlchemy to use `job_portal.sqlite3`. The `job_portal.db` file is also present in the repository, but it is not the database path configured in the current application code.

The `venv/` directory is your local virtual environment. It does not normally need to be uploaded to GitHub because the dependencies can be installed using `requirements.txt`.

---

## ⚙️ Installation and Setup

Follow these steps to run CareerHub on your local computer.

### Prerequisites

Make sure you have installed:

* Python 3.10 or later
* pip
* Git (optional, if downloading through Git)
* A web browser

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/nischith-ctrl/job_portal_project.git
```

Move into the project directory:

```bash
cd job_portal_project
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
```

Activate the environment in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Or activate it in Command Prompt:

```cmd
venv\Scripts\activate
```

If you are using macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

The main dependencies include Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug, Requests, and Gunicorn.

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

### 5. Open the Website

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

You can now explore CareerHub locally.

**Note:** The application initializes the database tables and creates sample users and job listings when necessary.

---

## 🔐 Demo Accounts

The application source code defines the following demonstration accounts for the initial database setup.

| Role          | Email                 | Password      |
| ------------- | --------------------- | ------------- |
| Administrator | `admin@jobportal.com` | `admin123`    |
| Employer      | `hr@techcorp.com`     | `employer123` |
| Job Seeker    | `john@example.com`    | `seeker123`   |

These credentials are intended for demonstration and testing only. They are created when the application initializes an empty database for the first time.

**Security warning:** Do not use these credentials in a production environment. Change or remove the demo accounts before making the application available for real users.

---

## 🔗 API Documentation

CareerHub provides a public endpoint that returns stored job listings as JSON.

### Get All Jobs

**Endpoint:**

```http
GET /api/jobs
```

**Local URL:**

```text
http://127.0.0.1:5000/api/jobs
```

**Live URL:**

https://job-portal-project-crnm.onrender.com/api/jobs

The response contains job information such as:

* Job ID
* Job title
* Company
* Category
* Location
* Salary
* Creation date

### External Job Import

The application also integrates with the Remotive API to import remote job listings.

Authorized employers and administrators can use the application's job-import feature from the dashboard.

---

## 🗄️ Database Design

CareerHub uses SQLite with Flask-SQLAlchemy to store application data.

The application defines three primary database models:

### 1. User

Stores account information, including:

* Username
* Email
* Hashed password
* User role

### 2. Job

Stores job listing information, including:

* Job title
* Company
* Category
* Location
* Salary
* Description
* Employer reference
* Creation date

### 3. Application

Stores job application information, including:

* Job reference
* Applicant reference
* Resume link
* Cover letter
* Application status
* Application date

Relationships between these models connect employers with their job listings and job seekers with their applications.

---


## 🎯 Project Objectives

The main objectives of CareerHub are to:

* Develop a full-stack web application using Python and Flask.
* Implement role-based authentication and access control.
* Build job search, posting, editing, and application workflows.
* Integrate an external API for importing job listings.
* Work with relational data using SQLite and SQLAlchemy.
* Deploy a Python web application on a cloud hosting platform.

---

## 👨‍💻 Author

**Nischith Shettigar**

GitHub: https://github.com/nischith-ctrl

---

## 📄 License

This project is available for educational and portfolio purposes. A formal open-source license has not yet been specified.
