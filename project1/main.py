import csv

list_of_all_errors = []
valid_records = [] # List of rows
invalid_records = [] # List of rows with errors

with open("employee_records_with_errors.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        row_errors = [] 
        # 1. First Name
        first_name = row[0]
        if not first_name.isalpha():
            row_errors.append("Error in First Name")
        # 2. last name
        last_name = row[1]
        if not last_name.isalpha():
            row_errors.append("Error in Last name")
        # 3. Date of Birth
        from datetime import datetime
        dob = row[2]
        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            min_date = datetime(1960, 1, 1)
            max_date = datetime(2005, 12, 31)
            if not (min_date <= dob_date <= max_date):
                row_errors.append("Error: Date of Birth out of range")
        except ValueError:
            row_errors.append("Error: Invalid Date of Birth format")
        #4. email
        email=row[3]
        import re

        pattern=r"^[a-zA-Z.0-9_]+@[a-zA-Z]+.[a-zA-Z]{2,}$"
        match = re.search(pattern, email)
        if not match:
            row_errors.append("Error: Invalid Email")
        #5. phone
        phone=row[4]
        pattern=r"^[6-9][0-9]{9}$"
        match= re.search(pattern, phone)
        if not match:
            row_errors.append("Error: invalid contact")
        #6.Employ id
        id=row[5]
        pattern=r"^EMP[0-9]{4}$"
        match=re.search(pattern,id)
        if not match:
            row_errors.append("Error: invalid id")
        #7. Department
        dept= row[6]
        allowed_dept=["HR", "IT", "Sales","Finance"]
        if dept not in allowed_dept:
            row_errors.append("Error: Invalid Department")
        #8. date of joining
        join_date = row[7]
        try:
            join_date = datetime.strptime(join_date, '%Y-%m-%d')
            min_date = datetime(2010, 1, 1)
            max_date = datetime(2025, 12, 31)
            if not (min_date <= join_date <= max_date):
                row_errors.append("Error: Date of joining")
        except ValueError:
            row_errors.append("Error: Invalid Date of joining format")
        #9.salary
        salary=row[8]
        try:
            salary=float(salary)
            if salary < 0:
                row_errors.append("Error: Invalid Salary")
        except ValueError:
            row_errors.append("Error: Incalid salary format")
        # 10. manager id
        manager_id=row[9]
        if not manager_id:
            pattern=r"^EMP[0-9]{4}$"
            match=re.search(pattern,manager_id)
            if not match:
                row_errors.append("Error: manager id")
        #11.status
        status=row[10]
        allowed_deptstatus=["Active","Inactive"]
        if status not in allowed_deptstatus:
            row_errors.append("Error: invalid condition")
        #12 gender
        gender=row[11]
        allowed_gender=["Male","Female","Other"]
        if gender not in allowed_gender:
            row_errors.append("Error: invalid gender")
        #13. pan card
        pan=row[12]
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$"
        match=re.search(pattern,pan)
        if not match:
            row_errors.append("Error:Invalid pan id")
        #14.adhaar
        adhaar=row[13]
        pattern=r"^[0-9]{12}$"
        match=re.search(pattern,adhaar)
        if not match:
            row_errors.append("Error: Invalid Adhaar Number")
        if row_errors:
            # Row was invalid
            row.append(row_errors)
            invalid_records.append(row)
        else:
            # Row was valid            
            valid_records.append(row)
        
    # for record in invalid_records:
    #     print(record)  
    #     print()       
    print("Total invalid records are", len(invalid_records))
    with open("invalid_employee_records.csv", "w", newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write header with an extra column for errors
        writer.writerow([
            "First Name", "Last Name", "Date of Birth", "Email", "Phone", "Employee ID",
            "Department", "Date of Joining", "Salary", "Manager ID", "Status", "Gender",
            "PAN Card", "Adhaar","Address", "Errors"
        ])
        for row in invalid_records:
            # Join errors as a single string
            row_to_write = row[:-1] + [", ".join(row[-1])]
            writer.writerow(row_to_write)

        import sqlite3
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
                adhaar TEXT,
                address TEXT
            )
        ''')

        # Insert valid records into the database
        for valid_row in valid_records:
            # If address column is missing, add empty string
            if len(valid_row) < 14:
                valid_row.append("")
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', valid_row)
            except Exception as e:
                print("Error inserting record:", e)

        conn.commit()
        conn.close()
    