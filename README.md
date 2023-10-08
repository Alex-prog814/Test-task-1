Quick Start Guide

1. Setting up a virtual environment

   After cloning the project, go to the project folder using the terminal and type the following command:

   ```
   python3.10 -m venv venv
   ```

   now activate the environment:

   ```
   source venv/bin/activate
   ```

2. Django must be installed, along with all required modules and third-party libraries
   Type the following command:
   ```
   pip3 install -r requirements.txt
   ```
   
3. You need to create a .env file in the root of the project, in which you must add the following data.
   This project uses postgresql, so you also need to provide database access credentials

   ```
   SECRET_KEY=generate_secret_key_here
   DB_USERNAME=your_username_from_db
   DB_NAME=db_name
   DB_PASSWORD=your_password_from_db
   ```

5. Migrations to the database

   Type the command in the terminal:

   ```
   python3 manage.py makemigrations
   ```

   then

   ```
    python3 manage.py migrate
   ```

6. Create superuser

   Enter the following command to create a superuser:

   ```
   python3 manage.py createsuperuser
   ```

   then enter the requested data


5. Before start,
   run fake data generator, this create 125 departments and 50 000 employees
   ```
   make generate_data
   ```
   Once completed, you will see a message in the terminal: Data generation complete!


6. Server start

   Enter the following command in terminal:

   ```
   python3 manage.py runserver
   ```

   Fine! Project is ready to use.


7. Short project description:

   In this small project you can see a tree of departments; by clicking on each of them, you can go to the page of the employees in this department. It is also possible to view a list of all employees by following the appropriate path. Creation and editing of employees and departments occurs in the admin area; a corresponding button has been added to the navbar.