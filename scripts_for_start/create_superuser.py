import os
import sys

def create_superuser():
    try:
        script = """
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created: admin@example.com / admin123')
else:
    print('Superuser already exists')
"""
        
        with open('/tmp/create_superuser.py', 'w') as f:
            f.write(script)
        
        result = os.system("python manage.py shell < /tmp/create_superuser.py")
        
        if os.path.exists('/tmp/create_superuser.py'):
            os.remove('/tmp/create_superuser.py')
        
        if result == 0:
            return True
        else:
            print('Error creating superuser')
            return False
    except Exception as e:
        print(f'Error creating superuser: {e}')
        return False

if __name__ == "__main__":
    success = create_superuser()
    sys.exit(0 if success else 1)