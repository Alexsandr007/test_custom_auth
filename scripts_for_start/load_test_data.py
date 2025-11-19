import os
import sys

def load_test_data():
    try:
        if os.path.exists("authentication/fixtures/initial_data.json"):
            result = os.system("python manage.py loaddata authentication/fixtures/initial_data.json")
            
            if result == 0:
                print('Test data loaded')
                return True
            else:
                print('Error loading test data')
                return False
        else:
            print('ℹNo initial_data.json found')
            return True
    except Exception as e:
        print(f'Error loading test data: {e}')
        return False

if __name__ == "__main__":
    success = load_test_data()
    sys.exit(0 if success else 1)