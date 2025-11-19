import os
import sys

sys.path.append('/app')

def run_migrations():
    try:
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")
        
        print('Migrations applied successfully')
        return True
    except Exception as e:
        print(f'Error running migrations: {e}')
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)