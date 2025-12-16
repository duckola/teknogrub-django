#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TeknoGrub.settings')
    
    # Custom command to set up the project
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        print("--- Setting up the project ---")
        
        # 1. Create the database
        print("\n--- Creating database ---")
        try:
            subprocess.run([sys.executable, 'create_db.py'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Error during database creation: {e}")
            sys.exit(1)
            
        # 2. Run migrations
        print("\n--- Running migrations ---")
        try:
            execute_from_command_line([sys.argv[0], 'migrate'])
        except Exception as e:
            print(f"Error during migrations: {e}")
            sys.exit(1)
            
        # 3. Seed the data
        print("\n--- Seeding data ---")
        try:
            execute_from_command_line([sys.argv[0], 'seed_data'])
        except Exception as e:
            print(f"Error during data seeding: {e}")
            sys.exit(1)
            
        print("\n--- Project setup complete! ---")
        sys.exit(0)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
