import os
import sys

def collect_static():
    try:
        result = os.system("python manage.py collectstatic --noinput")
        
        if result == 0:
            print('Static files collected')
            return True
        else:
            print('Error collecting static files')
            return False
    except Exception as e:
        print(f'Error collecting static files: {e}')
        return False

if __name__ == "__main__":
    success = collect_static()
    sys.exit(0 if success else 1)