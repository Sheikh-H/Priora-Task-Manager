**PLEASE DO NOT USE REAL DATA, DEMO PURPOSES ONLY**
---
# ✅ Priora: Full-Stack Task Management Application

<p align="center">
  <b>A full-stack task management application built with Flask, SQLite, JavaScript, and modern web development practices.</b><br>
  Designed as a portfolio project to demonstrate backend development, database design, security implementation, and structured application architecture. This project is actively maintained and will continue to receive improvements as I expand my understanding of full-stack development.
</p>

---

# 📘 Project Overview

Priora is a full-stack task management application developed to demonstrate my progression from creating simple websites into building complete web applications with a backend, database, authentication system, and structured code architecture.

The purpose of this project is to create a realistic productivity application where users can create accounts, manage personal tasks, track progress, and maintain a history of task activity.

This project is built for **portfolio and educational purposes only**. It demonstrates my understanding of full-stack development concepts and is not intended to be used as a commercial productivity platform.

The main goal behind Priora was not only to create a functional application, but to understand how real-world applications are structured, maintained, and secured.

---

# 🚀 Development Journey

Priora represents an important stage in my development journey because it combines the frontend skills I previously developed with new backend and software engineering concepts.

Earlier projects focused mainly on creating visually appealing websites using HTML, CSS, and JavaScript. While those projects helped me understand layouts, styling, responsiveness, and user interaction, I wanted to move towards building applications that could store data, manage users, and perform real operations.

This project allowed me to learn:

- How frontend and backend systems communicate.
- How databases store and organise application data.
- How authentication systems work.
- How user data can be protected.
- How larger projects should be structured for maintainability.

One of the biggest improvements I made during this project was how I organise my CSS.

Instead of keeping all styling inside one large stylesheet, I began separating CSS into sections based on purpose and page requirements. This made development much easier because:

- Individual pages are easier to maintain.
- Changes are easier to locate.
- Styling conflicts are reduced.
- The project structure becomes clearer as the application grows.

This approach reflects how larger applications are often organised, where different components and features have their own responsibilities.

---

# ✨ Features

## 👤 User Accounts

Priora includes a complete authentication system allowing users to:

- Create an account.
- Securely log in.
- Reset their password.
- Change their password.
- Log out securely.
- Access only their own tasks.

Each user has their own private task data which is separated through database relationships.

---

## ✅ Task Management

Users can:

- Create new tasks.
- View upcoming tasks.
- View overdue tasks.
- View today's tasks.
- Update task information.
- Delete tasks.
- Mark tasks as complete or incomplete.
- Search and filter tasks.

The application tracks task information including:

- Title.
- Description.
- Due date.
- Due time.
- Completion date.
- Completion status.

---

## 📋 Task History

A major feature of Priora is task logging.

The application records important task events, including:

- Task creation.
- Task completion.
- Task reopening.
- Task updates.
- User-added notes.

This creates an activity history, allowing users to understand how tasks have changed over time.

---

## 🌙 User Interface

The frontend includes:

- Responsive design.
- Dark mode support.
- Animated page elements.
- Client-side form validation.
- Dynamic interface updates.
- Mobile-friendly layouts.

JavaScript is used to improve user experience without replacing server-side validation.

---

# 🏗️ Application Architecture

Priora follows a structured Flask application design by separating responsibilities into different files.

```
Priora/
│
├── app.py                         # Main Flask application and route handling
├── requirements.txt               # Project dependencies
├── README.md                      # Project documentation
├── LICENSE                        # MIT Licence
│
├── instance/
│   └── task-manager.db            # SQLite database (auto generated)
│
├── services/                      # Backend application services
│   ├── auth.py                    # Authentication and password security
│   ├── config.py                  # Application initialisation
│   ├── database.py                # Database connections and CRUD operations
│   └── tasks.py                   # Task management logic
│
├── templates/                     # Jinja HTML templates
│   ├── layout.html                # Base application layout
│   ├── main/                      # Public pages
│   ├── user/                      # User account pages
│   ├── tasks/                     # Task management pages
│   └── error/                     # Error handling pages
│
├── static/                        # Frontend assets
│   │
│   ├── css/
│   │   ├── base.css               # Global styling and variables
│   │   ├── animations.css         # Page animations
│   │   ├── responsive.css         # Responsive layouts
│   │   ├── components/            # Reusable component styles
│   │   └── pages/                 # Page-specific styling
│   │
│   ├── js/
│   │   └── script.js              # Client-side functionality
│   │
│   └── media/                     # Images, icons and backgrounds
│
└── .env                           # Environment variables (auto generated)
```

---

## ⚙️ How The Application Works

### Flask Routes (`app.py`)

The Flask application acts as the connection between the user interface and backend services.

Routes handle requests such as:

- Loading pages.
- Processing forms.
- Creating tasks.
- Updating tasks.
- Authenticating users.

For example:

```python
@app.route("/user/tasks/add-task")
```
handles requests for creating new tasks.

The route receives user input, validates the information, then communicates with the database service.

### 🗄️ Database Layer (database.py)

The database service manages communication with SQLite.

It contains functions responsible for:

- Creating database tables.
- Adding users.
- Searching users.
- Creating tasks.
- Updating tasks.
- Removing tasks.
- Retrieving task history.

Using a separate database layer keeps SQL operations away from application routes, making the project easier to maintain.

### 📝 Task Service (tasks.py)

The task service sits between the Flask routes and database.

Its purpose is to handle task-related logic.

Examples:

### Loading Tasks

Retrieves active tasks belonging to the logged-in user.

### Searching Tasks

Allows tasks to be filtered by:

- Date.
- Completion status.
- Task ID.
- Completing Tasks

Updates the task status and creates a log entry recording the change.

Separating this logic prevents app.py from becoming too large and difficult to manage.

## 🛡️ Security Implementation

Security was an important learning area during this project.

Although Priora is a portfolio project, I wanted to implement practices used in professional applications.

### Password Protection

Passwords are never stored as plain text.

Priora uses:

- Argon2 password hashing.
- Secure password verification.
- Password reset protection.

Argon2 is designed specifically for password security and helps protect user credentials if database information is exposed.

### Session Security

User sessions are protected using Flask session management.

Implemented security features include:

- HTTP-only cookies.
- Secure cookies.
- SameSite cookie restrictions.
- Session expiration.
- Protected routes.
- CSRF Protection

Priora uses Flask-WTF CSRF protection.

Sensitive actions require valid CSRF tokens, including:

- Logging out.
- Creating tasks.
- Updating tasks.
- Deleting tasks.
- Changing task completion status.

This helps prevent malicious websites from submitting unwanted requests on behalf of users.

### Database Security

Database security measures include:

- Parameterised SQL queries.
- Foreign key relationships.
- User ownership checks.
- SQLite foreign key enforcement.

Users can only access and modify their own tasks.

### Content Security Policy

The application includes security headers using Content Security Policy (CSP).

This restricts where scripts, styles, and resources can be loaded from, helping reduce certain browser-based attacks.

# 🧩 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Backend programming language powering the application logic. |
| **Flask** | Lightweight web framework handling routing, requests, templates, and application structure. |
| **SQLite** | Database engine used to store users, tasks, and task history. |
| **Jinja** | Server-side templating engine used to dynamically generate HTML pages. |
| **HTML5** | Provides the structure and semantic layout of the website. |
| **CSS3** | Handles styling, responsive layouts, animations, and theme support. |
| **JavaScript** | Provides client-side functionality, validation, animations, and interactive features. |
| **Argon2** | Secure password hashing algorithm used to protect user credentials. |
| **Flask-WTF** | Provides CSRF protection for secure form submissions. |
| **Gunicorn** | Production WSGI server used for deploying the Flask application. |

## 🗄️ Database Design

Priora uses three main database tables.

### Users Table

Stores account information.

- user_id
- first_name
- last_name
- email
- password
- date_created

### Tasks Table

Stores user tasks.

- task_id
- user_id
- title
- description
- due_date
- due_time
- completed
- completion_date
- completion_time

## Requirements

- Python 3.10+
- pip
- Virtual environment

## Installation

Clone the repository:

`git clone <repository-url>`

Navigate into the project:

`cd Priora`

Create a virtual environment:

`python -m venv venv`

Activate the environment:

`source venv/bin/activate`

Install dependencies:

`pip install -r requirements.txt`

Create your environment variables:

`SECRET_KEY=your_secret_key`

Run Flask:

`flask run`

## ☁️ Deployment

Priora is designed to be deployed using platforms such as Render.

Production deployments can use Gunicorn:

`gunicorn app:app`

Environment variables should be stored securely through the hosting provider.

## 🔮 Future Improvements

Possible future improvements include:

- Migrating from SQLite to PostgreSQL.
- Adding task categories.
- Adding task priority levels.
- Adding email notifications.
- Adding automated testing.
- Adding database migrations.
- Creating a mobile application.
- Improving accessibility features.
- Adding user profile management.
- Improving task sorting options.
- Adding API endpoints.
- Adding automated deployment pipelines.

---

## 📄 Licence

<p>
  This project is licensed under the <b>MIT Licence</b> — see the <a href="./LICENCE">LICENCE</a> file for details.
</p>

<pre>
MIT Licence

Copyright (c) 2026 Sheikh Hussain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>

---

## Footnote

<div align="center" style="border: 1px solid green; padding: 10px; border-radius: 5px;">
  <p>🗣️ Feel free to follow, connect, and chat!</p>
  <a class="header-badge" target="_blank" href="https://github.com/Sheikh-H"><img src="https://img.shields.io/badge/GitHub-376e00?style=flat&logo=github&logoColor=white" alt="GitHub"></a>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/sheikh-hussain/"><img src="https://img.shields.io/badge/LinkedIn-376e00?style=flat&logo=LinkedIn&logoColor=white" alt="LinkedIn"></a>
  <a class="header-badge" target="_blank" href="mailto:sheikh.hussain1155@gmail.com"><img src="https://img.shields.io/badge/Gmail-376e00?style=flat&logo=gmail&logoColor=white" alt="Gmail"></a>
  <a class="header-badge" target="_blank" href="https://sheikh-hussain.onrender.com/"><img src="https://img.shields.io/badge/Portfolio-376e00?style=flat&logo=github&logoColor=white" alt="Portfolio"></a>
</div>

<div align="center">
  <a href="https://sheikh-hussain.onrender.com/" target="_blank">By Sheikh Hussain 💚</a>
</div>
