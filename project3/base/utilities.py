import sqlite3

def delete_employee(id):
    conn = sqlite3.connect("employee_records.db")
    cursor = conn.cursor()
    try:
        cursor.execute('delete from employees where employee_id=?', (id,))
    except Exception as e:
        raise ValueError(f"Error Deleting record {e}")
    conn.commit()
    conn.close()



def view_employees():
    # 1. Make DB Connection
    # 2. Make cursor
    # 3. Execute Query
    # 4. Close Connection
    # 5. Return Result 
    conn = sqlite3.connect('employee_records.db') 
    cursor = conn.cursor()
    try:
        employees = cursor.execute('''
                select * from employees  
                ''').fetchall()
       #convert tuple into dict
        employees = [dict(zip([column[0] for column in cursor.description], row)) for row in employees]
    except Exception as e:
        print("Error viewing record:", e)
        raise ValueError(f"Error viewing record: {e}")
    conn.commit()
    conn.close()
    return employees


def save_employee(record):
    row_errors = [] 

    # 1. First Name
    first_name = record['FirstName']
    if not first_name.isalpha():
        row_errors.append("Error in First Name")
    # 2. last name
    last_name = record['LastName']
    if not last_name.isalpha():
        row_errors.append("Error in Last name")
    # 3. Date of Birth
    from datetime import datetime
    dob = record['dob']
    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        min_date = datetime(1960, 1, 1)
        max_date = datetime(2005, 12, 31)
        if not (min_date <= dob_date <= max_date):
            row_errors.append("Error: Date of Birth out of range")
    except ValueError:
        row_errors.append("Error: Invalid Date of Birth format")
    #4. email
    email=record['email']
    import re

    pattern=r"^[a-zA-Z.0-9_]+@[a-zA-Z]+.[a-zA-Z]{2,}$"
    match = re.search(pattern, email)
    if not match:
        row_errors.append("Error: Invalid Email")
    #5. phone
    phone=record['Contact']
    pattern=r"^[6-9][0-9]{9}$"
    match= re.search(pattern, phone)
    if not match:
        row_errors.append("Error: invalid contact")
    #6.Employ id
    id=record["employeID"]
    pattern=r"^EMP[0-9]{4}$"
    match=re.search(pattern,id)
    if not match:
        row_errors.append("Error: invalid id")
    #7. Department
    dept= record['departmentId']
    allowed_dept=["HR", "IT", "Sales","Finance"]
    if dept not in allowed_dept:
        row_errors.append("Error: Invalid Department")
    #8. date of joining
    join_date = record['joiningdate']
    try:
        join_date = datetime.strptime(join_date, '%Y-%m-%d')
        min_date = datetime(2010, 1, 1)
        max_date = datetime(2025, 12, 31)
        if not (min_date <= join_date <= max_date):
            row_errors.append("Error: Date of joining")
    except ValueError:
        row_errors.append("Error: Invalid Date of joining format")
    #9.salary
    salary=record["Salary"]
    try:
        salary=float(salary)
        if salary < 0:
            row_errors.append("Error: Invalid Salary")
    except ValueError:
        row_errors.append("Error: Incalid salary format")
    # 10. manager id
    manager_id=record['managerId']
    if not manager_id:
        pattern=r"^EMP[0-9]{4}$"
        match=re.search(pattern,manager_id)
        if not match:
            row_errors.append("Error: manager id")
    #11.status
    status=record["Status"]
    allowed_deptstatus=["Active","Inactive"]
    if status not in allowed_deptstatus:
        row_errors.append("Error: invalid condition")
    #12 gender
    gender=record["Gender"]
    allowed_gender=["Male","Female","Other"]
    if gender not in allowed_gender:
        row_errors.append("Error: invalid gender")
    #13. pan card
    pan=record["panId"]
    pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    match=re.search(pattern,pan)
    if not match:
        row_errors.append("Error:Invalid pan id")
    #14.adhaar
    adhaar=record["AadharId"]
    pattern=r"^[0-9]{12}$"
    match=re.search(pattern,adhaar)
    if not match:
        row_errors.append("Error: Invalid Adhaar Number")

    if row_errors:
        # Row was invalid
        raise ValueError(row_errors)
    else:
        # If record is valid, then save to DB
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('employee_records.db')
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                first_name TEXT,
                last_name TEXT,
                dob TEXT,
                email TEXT,
                phone TEXT,
                employee_id TEXT PRIMARY KEY,
                department TEXT,
                join_date TEXT,
                salary REAL,
                manager_id TEXT,
                status TEXT,
                gender TEXT,
                pan TEXT,
                adhaar TEXT
          )
        ''')

        # Save to DB
        try:
            values = [
                record['FirstName'],
                record['LastName'],
                record['dob'],
                record['email'],
                record['Contact'],
                record['employeID'],
                record['departmentId'],
                record['joiningdate'],
                float(record['Salary']),
                record['managerId'],
                record['Status'],
                record['Gender'],
                record['panId'],
                record['AadharId']
            ]
            cursor.execute('''
                INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
        except Exception as e:
            print("Error inserting record:", e)
            raise ValueError(f"Error inserting record: {e}")
        conn.commit()
        conn.close()