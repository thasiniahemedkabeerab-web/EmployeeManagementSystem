import sqlite3
import os
import platform

# ------------------ UTILITY ------------------

def clear_screen():
    """Clear the terminal screen"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def pause():
    input("\nPress Enter to continue...")

# ------------------ DATABASE CONNECTION ------------------

def connect_db():
    return sqlite3.connect("employee.db")


# ------------------ CREATE TABLES ------------------

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments(
        dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dept_name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        salary REAL,
        dept_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY(dept_id) REFERENCES departments(dept_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()


# ------------------ INITIAL SETUP ------------------

def initial_setup():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    if count == 0:
        clear_screen()
        print("="*40)
        print("=== Initial Setup: Create Admin User ===")
        print("="*40)
        while True:
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users(username,password,role) VALUES(?,?,?)",
                    (username, password, "admin")
                )
                conn.commit()
                conn.close()
                print("\nAdmin user created successfully!\n")
                pause()
                break
            except sqlite3.IntegrityError:
                print("Username already exists! Try again.")
            except Exception as e:
                print("Error:", e)


# ------------------ LOGIN ------------------

def login_menu():
    while True:
        clear_screen()
        print("="*40)
        print("=== LOGIN MENU ===")
        print("="*40)
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role,user_id FROM users WHERE username=? AND password=?",
                (username, password)
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                print("\nLogin Successful!\n")
                pause()
                return result
            else:
                print("\nUsername or password is incorrect!")
                print("1 Retry Login")
                print("2 Exit")
                choice = input("Enter choice: ")
                if choice == "1":
                    continue
                elif choice == "2":
                    return None
                else:
                    print("Invalid choice, retrying login...")
                    pause()
        except Exception as e:
            print("Error:", e)
            pause()
            return None


# ------------------ USERS ------------------

def add_user():
    clear_screen()
    print("="*40)
    print("=== ADD USER ===")
    print("="*40)
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (admin/employer/employee): ").lower()
        if role not in ["admin","employer","employee"]:
            print("Invalid role! Must be admin, employer, or employee.")
            pause()
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username,password,role)
        )

        conn.commit()
        conn.close()
        print("User Added Successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    except Exception as e:
        print("Error:", e)
    pause()


# ------------------ DEPARTMENTS ------------------

def add_department():
    clear_screen()
    print("="*40)
    print("=== ADD DEPARTMENT ===")
    print("="*40)
    try:
        name = input("Enter Department Name: ")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO departments(dept_name) VALUES(?)",(name,))
        conn.commit()
        conn.close()
        print("Department Added Successfully!")
    except sqlite3.IntegrityError:
        print("Department already exists!")
    except Exception as e:
        print("Error:", e)
    pause()


def view_departments():
    clear_screen()
    print("="*40)
    print("=== DEPARTMENTS LIST ===")
    print("="*40)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No departments found")
        else:
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]}")
    except Exception as e:
        print("Error:", e)
    pause()


# ------------------ EMPLOYEES ------------------

def add_employee():
    clear_screen()
    print("="*40)
    print("=== ADD EMPLOYEE ===")
    print("="*40)
    try:
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        salary = float(input("Enter Salary: "))

        view_departments()
        dept_id = int(input("Enter Department ID: "))

        # List available users with employee role
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE role='employee'")
        users = cursor.fetchall()
        if not users:
            print("No employee users found. Add a user first.")
            conn.close()
            pause()
            return

        print("\nAvailable Employee Users:")
        for u in users:
            print(f"ID: {u[0]} | Username: {u[1]}")
        user_id = int(input("Enter User ID to link with this employee: "))

        cursor.execute("""
        INSERT INTO employees(name,age,salary,dept_id,user_id)
        VALUES(?,?,?,?,?)
        """,(name,age,salary,dept_id,user_id))

        conn.commit()
        conn.close()
        print("Employee Added Successfully!")
    except ValueError:
        print("Invalid input! Please enter correct data types.")
    except Exception as e:
        print("Error:", e)
    pause()


def view_employees():
    clear_screen()
    print("="*40)
    print("=== EMPLOYEES LIST ===")
    print("="*40)
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT emp_id,name,age,salary,dept_name,username
        FROM employees
        JOIN departments ON employees.dept_id = departments.dept_id
        JOIN users ON employees.user_id = users.user_id
        """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No employees found")
        else:
            for row in rows:
                print(f"ID:{row[0]} | Name:{row[1]} | Age:{row[2]} | Salary:{row[3]} | Dept:{row[4]} | User:{row[5]}")
    except Exception as e:
        print("Error:", e)
    pause()


def update_employee():
    clear_screen()
    print("="*40)
    print("=== UPDATE EMPLOYEE SALARY ===")
    print("="*40)
    try:
        emp_id = int(input("Enter Employee ID to update salary: "))
        new_salary = float(input("Enter New Salary: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE employees SET salary=? WHERE emp_id=?",
            (new_salary,emp_id)
        )

        if cursor.rowcount == 0:
            print("Employee not found")
        else:
            print("Employee Updated Successfully!")

        conn.commit()
        conn.close()
    except ValueError:
        print("Invalid input! Enter numbers only.")
    except Exception as e:
        print("Error:", e)
    pause()


def delete_employee():
    clear_screen()
    print("="*40)
    print("=== DELETE EMPLOYEE ===")
    print("="*40)
    try:
        emp_id = int(input("Enter Employee ID to delete: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM employees WHERE emp_id=?",(emp_id,))
        if cursor.rowcount == 0:
            print("Employee not found")
        else:
            print("Employee Deleted Successfully!")

        conn.commit()
        conn.close()
    except ValueError:
        print("Invalid input! Enter a valid ID.")
    except Exception as e:
        print("Error:", e)
    pause()


# ------------------ PROFILE ------------------

def view_profile(user_id):
    clear_screen()
    print("="*40)
    print("=== MY PROFILE ===")
    print("="*40)
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT name,age,salary,dept_name
        FROM employees
        JOIN departments ON employees.dept_id = departments.dept_id
        WHERE user_id=?
        """,(user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            print(f"Name: {row[0]}\nAge: {row[1]}\nSalary: {row[2]}\nDepartment: {row[3]}")
        else:
            print("Profile not found")
    except Exception as e:
        print("Error:", e)
    pause()


# ------------------ MENUS ------------------

def admin_menu():
    while True:
        clear_screen()
        print("="*40)
        print("=== ADMIN MENU ===")
        print("="*40)
        print("1 Add User")
        print("2 Add Department")
        print("3 View Departments")
        print("4 Add Employee")
        print("5 View Employees")
        print("6 Update Employee Salary")
        print("7 Delete Employee")
        print("8 Logout")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_user()
        elif choice == "2":
            add_department()
        elif choice == "3":
            view_departments()
        elif choice == "4":
            add_employee()
        elif choice == "5":
            view_employees()
        elif choice == "6":
            update_employee()
        elif choice == "7":
            delete_employee()
        elif choice == "8":
            break
        else:
            print("Invalid Choice")
            pause()


def employer_menu():
    while True:
        clear_screen()
        print("="*40)
        print("=== EMPLOYER MENU ===")
        print("="*40)
        print("1 View Employees")
        print("2 Update Employee Salary")
        print("3 Logout")

        choice = input("Enter Choice: ")

        if choice == "1":
            view_employees()
        elif choice == "2":
            update_employee()
        elif choice == "3":
            break
        else:
            print("Invalid Choice")
            pause()


def employee_menu(user_id):
    while True:
        clear_screen()
        print("="*40)
        print("=== EMPLOYEE MENU ===")
        print("="*40)
        print("1 View My Profile")
        print("2 Logout")

        choice = input("Enter Choice: ")

        if choice == "1":
            view_profile(user_id)
        elif choice == "2":
            break
        else:
            print("Invalid Choice")
            pause()


# ------------------ MAIN ------------------

def main():
    create_tables()
    initial_setup()  # <-- Create first admin if no users exist

    while True:
        clear_screen()
        print("="*40)
        print("=== EMPLOYEE MANAGEMENT SYSTEM ===")
        print("="*40)
        print("1 Login")
        print("2 Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            result = login_menu()
            if result:
                role, user_id = result
                if role == "admin":
                    admin_menu()
                elif role == "employer":
                    employer_menu()
                elif role == "employee":
                    employee_menu(user_id)
        elif choice == "2":
            print("\nExiting Program...")
            break
        else:
            print("Invalid Choice")
            pause()


# ------------------ RUN ------------------

if __name__ == "__main__":
    main()