# School-Management-System

This app is meant to be used by school manager to manage their school records:
* student data
* staff
* results
* finances

It runs Django Framework in back-end and HTML, CSS in front-end. It has a interactive dashboard built in for admin using which admin can add student, manage fees , manage employees, manage results .

## Features Of This Project
* Academy Management - Manage Session , Terms, Subjects, Classes.
* Student Management -  Add Student , Bulk Add Student,  Fees Details Check , View Profile.
* Employee Management - Add Employee, Edit Employee, View Employee.
* Fees Management -  Add Fees , Delete Fees, Pay fee , Fees Structure , customize fee Structure.
* Result Management -  Add Result , Edit Result , Manage Result.

## Development status
It currently doesn't allow students/staff to login.
Solely, it's expected to be used on a single machine or online for managers only.


username: admin
password: admin123
```


Run

```python
pip install -r requirements.txt #install required packages
python manage.py migrate # run first migration
python manage.py seed_demo_data # optional: load demo students, results and an invoice
python manage.py runserver # run the server
```
Then locate http://172.0.0.1:8000

## Admin Login
When you run migrate, a superuser is created.
```bash
username: admin
password: admin123
```

## Roadmap
To build a fully fledged open source school management.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Coding Standards
```bash
isort .
black .
```

## Test
```base
python manage.py test
```
