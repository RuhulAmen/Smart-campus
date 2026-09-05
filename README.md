# 🏫 Smart Campus Utility & Maintenance Management System

A full-stack web application built with **Flask** and **MongoDB Atlas** to manage campus facilities, report maintenance issues, and view real-time announcements.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)
![JWT](https://img.shields.io/badge/JWT-Auth-orange)
![HTML5](https://img.shields.io/badge/HTML5-CSS3-purple)

---

## 🚀 Features

- **🔐 Secure Authentication:** JWT-based signup/login with bcrypt password hashing and role-based access control (Student/Admin)
- **🏢 Facilities Management:** Real-time status tracking for campus facilities (operational, maintenance, closed)
- **⚠️ Issue Reporting:** Submit maintenance requests with automatic announcement generation
- **📢 Announcements System:** Priority-based campus-wide announcements with filtering
- **📊 User Dashboard:** Personalized stats dashboard showing facility status, issue counts, and recent announcements
- **📋 Issue Tracking:** Look up the status of your reported issues by email (My Reports page)
- **👤 Profile Management:** View and edit your name, email, student ID, and password
- **🛠️ Admin Panel:** Dedicated admin UI for managing facilities, publishing announcements, and updating issue statuses (role-protected)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.10+, Flask 3.0+ |
| **Database** | MongoDB Atlas (Cloud) + Flask-PyMongo |
| **Authentication** | JWT (PyJWT), Bcrypt |
| **API Security** | Flask-CORS, Custom auth decorators |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Environment** | Dotenv for config management |

---

## 📂 Project Structure

```text
Smart Campus Project/
├── backend/
│   ├── models/          # Data models (User, Facility, Issue, Announcement)
│   ├── routes/          # RESTful API endpoints with blueprints
│   ├── utils/           # JWT helpers, auth decorators, token management
│   ├── app.py           # Flask app entry point & CORS config
│   ├── create_admin.py  # CLI script to provision the first admin account
│   └── config.py        # Environment-based configuration
├── frontend/
│   ├── CSS/style.css    # Dark-themed responsive stylesheet
│   ├── js/app.js        # API client, auth logic, UI helpers
│   ├── index.html       # Landing page with facility preview
│   ├── login.html       # Authentication page
│   ├── signup.html      # User registration
│   ├── dashboard.html   # Stats & announcements dashboard
│   ├── facilities.html  # Facility status grid
│   ├── announcements.html # Announcements with filtering
│   ├── report-issue.html # Issue submission form
│   ├── my-reports.html  # Track reported issues by email
│   ├── profile.html     # Edit profile / change password
│   └── admin.html       # Admin panel (facilities, announcements, issues)
├── .env.example         # Environment template (copy to .env)
└── README.md

---

## 🔑 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/signup` | Register new user | No |
| `POST` | `/api/auth/login` | User login | No |
| `GET` | `/api/auth/verify` | Verify JWT token | Yes |
| `GET` | `/api/auth/profile` | Get user profile | Yes |
| `PUT` | `/api/auth/profile` | Update profile | Yes |
| `GET` | `/api/facilities` | List all facilities | No |
| `POST` | `/api/facilities` | Create facility | Admin |
| `PUT` | `/api/facilities/:id` | Update facility | Admin |
| `PATCH` | `/api/facilities/:id/status` | Update status | Admin |
| `DELETE` | `/api/facilities/:id` | Soft-delete facility | Admin |
| `GET` | `/api/announcements` | List announcements | No |
| `GET` | `/api/announcements/recent` | Recent announcements | No |
| `POST` | `/api/announcements` | Create announcement | Admin |
| `GET` | `/api/issues` | List all issues | No |
| `POST` | `/api/issues` | Report new issue | No |
| `GET` | `/api/issues/track?email=` | Track issues by reporter email | No |
| `GET` | `/api/issues/stats` | Issue status counts | No |
| `PATCH` | `/api/issues/:id/status` | Update issue status | Admin |
| `GET` | `/api/dashboard/stats` | Dashboard statistics | Yes |

---

## 🏗️ Key Technical Decisions

- **JWT Authentication:** Stateless auth using PyJWT with configurable expiration
- **Role-Based Access:** Custom `@token_required` and `@admin_required` decorators
- **No Self-Escalation:** Signup always assigns the `student` role; admins are provisioned via `create_admin.py`
- **Soft Deletes:** Facilities and announcements use `is_active`/`status` flags instead of hard deletion
- **Blueprint Architecture:** Modular route organization for scalability
- **Environment Variables:** Sensitive config (MongoDB URI, SECRET_KEY) loaded from `.env`

---

## 🚀 Getting Started

### 1. Clone & Install

```bash
# Install dependencies
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your MongoDB credentials and secret key
```

### 3. Create the First Admin Account

Self-service signups always create **student** accounts. To get an admin account (needed for the Admin Panel), run:

```bash
cd backend
python create_admin.py --email admin@campus.edu --password 'choose-a-strong-password'
```

You can also set `ADMIN_EMAIL`/`ADMIN_PASSWORD` in your `.env` and run the script without arguments.

### 4. Run the Application

```bash
python app.py
```

The app will be available at `http://localhost:5000`

---

## 📸 Screenshots

*(Add your screenshots here!)*

---

