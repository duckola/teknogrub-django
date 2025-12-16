import pymysql
import os
import subprocess
import sys

# Database connection parameters
db_user = 'root'
db_password = os.environ.get('DB_PASSWORD', 'password')
db_host = '127.0.0.1'
db_port = 3306
db_name = 'teknogrub_db'

def create_database():
    try:
        # Connect to MySQL server (without specifying a database)
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port
        )
        
        cursor = connection.cursor()
        
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created successfully (or already exists).")
        
        cursor.close()
        connection.close()
        return True

    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def run_migrations():
    print("Running migrations...")
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)

def create_users():
    print("Creating users...")
    # We'll use a management command or a script to create users using Django's ORM
    # But since we are outside of Django context here, it's better to run a separate script
    # or use 'shell' command.
    
    # Let's create a temporary script to create users
    user_creation_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TeknoGrub.settings')
django.setup()

from django.contrib.auth import get_user_model
from User.models import Role

User = get_user_model()

def create_role(name):
    role, created = Role.objects.get_or_create(role_name=name)
    return role

def create_user(username, password, role_name, email, first_name, last_name, is_superuser=False, is_staff=False):
    if not User.objects.filter(username=username).exists():
        role = create_role(role_name)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            id_number=username # Assuming username is ID number for simplicity here
        )
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.save()
        print(f"User '{username}' created.")
    else:
        print(f"User '{username}' already exists.")

# # Create Admin
# create_user('admin', 'admin123', 'Admin', 'admin@example.com', 'Admin', 'User', is_superuser=True, is_staff=True)

# Create Staff
create_user('staff', 'staff123', 'Staff', 'staff@example.com', 'Staff', 'User', is_staff=True)

# Create Student
create_user('student', 'student123', 'Student', 'student@example.com', 'Student', 'User')

"""
    with open('create_users_temp.py', 'w') as f:
        f.write(user_creation_script)
        
    subprocess.run([sys.executable, 'create_users_temp.py'], check=True)
    os.remove('create_users_temp.py')

if __name__ == "__main__":
    if create_database():
        run_migrations()
        create_users()
        print("Setup complete.")
