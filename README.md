# Employee Management System (Python & SQLite3)

## Project Overview

This is a **command-line Employee Management System** built using Python and SQLite3.  
It allows management of **users, departments, and employees** with role-based authentication:

- **Admin:** Can add users, departments, employees, view, update, and delete employees.  
- **Employer:** Can view employees and update salaries.  
- **Employee:** Can view their own profile.

The system uses a **SQLite3 database** for persistent storage and has a **CLI (Command-Line Interface)** for user interaction.

---

## Features

- User authentication (Admin, Employer, Employee)
- Role-based menus and permissions
- Add/View Departments
- Add/View/Update/Delete Employees
- View Employee Profile
- Exception handling for invalid inputs and database errors
- Clear CLI interface with menus and headers

---

## Requirements

- Python 3.x
- SQLite3 (built-in with Python)
- OS: Windows, Linux, or Mac

---

## Setup Instructions

1. **Clone or Download the Project**
   - Download the `.py` file (e.g., `ems.py`) to your local machine.

2. **Install Python**
   - Make sure Python 3.x is installed.
   - Verify by running:
     ```bash
     python --version
     ```

3. **Run the Program**
   - Open terminal / command prompt.
   - Navigate to the folder where the Python file is saved.
   - Run the program
   - The program will automatically create the SQLite database (`employee.db`) in the same folder.

4. **Initial Admin Setup**
   - If this is the first time running the program, it will prompt you to **create an admin user**.
   - Enter the admin **username** and **password**.
   - ex: admin, admin123

5. **Login**
   - Choose **Login** from the main menu.
   - Enter your **username** and **password**.
   - If credentials are incorrect, the system allows retry or exit.

6. **Navigating Menus**
   - Admin, Employer, and Employee have separate menus.
   - Admin can add users, departments, employees, view and modify employee data.
   - Employer can view employees and update salaries.
   - Employee can view their own profile.

