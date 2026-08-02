# 🏫 Smart Campus Utility & Maintenance Management System

A full-stack web application built with **Flask** and **MongoDB Atlas** to manage campus facilities, report maintenance issues, and view real-time announcements.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-lightgrey)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)

---

## 🚀 Features

- **User Authentication:** Secure Signup and Login using JWT (JSON Web Tokens) and Bcrypt hashing.
- **Facilities Management:** View real-time status and details of campus facilities.
- **Issue Reporting:** Students and staff can submit maintenance requests for specific facilities.
- **Announcements:** View campus-wide announcements.
- **User Dashboard:** View personalized statistics and user profile information.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-PyMongo, Flask-CORS
- **Database:** MongoDB Atlas (Cloud)
- **Authentication:** JWT, Bcrypt
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Environment:** WSL, Conda

---

## 📂 Project Structure

```text
Smart Campus Project/
├── backend/
│   ├── models/          # Database models (User, Facility, Issue, Announcement)
│   ├── routes/          # API route handlers (Auth, Dashboard, Facilities, etc.)
│   ├── utils/           # Helper functions (JWT generation, token verification)
│   ├── app.py           # Main Flask application entry point
│   └── config.py        # Application configuration
├── frontend/
│   ├── CSS/             # Stylesheets
│   ├── js/              # Frontend JavaScript
│   ├── index.html       # Homepage
│   ├── login.html       # Login page
│   ├── signup.html      # Signup page
│   └── ...              # Other HTML pages
├── .env             # Environment variables (MongoDB URI, Secret Key)
└── README.md
