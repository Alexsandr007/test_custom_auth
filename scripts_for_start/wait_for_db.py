import socket
import time
import os
import sys

def wait_for_database():
    host = os.environ.get('DATABASE_HOST')
    port = int(os.environ.get('POSTGRES_PORT', 5432))
    
    print(f"Waiting for database at {host}:{port}...")
    
    for i in range(30):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((host, port))
            print('Database is ready!')
            return True
        except Exception as e:
            if i == 0:
                print('Waiting for database...')
    
    print('Database connection failed after 30 seconds')
    return False

if __name__ == "__main__":
    success = wait_for_database()
    sys.exit(0 if success else 1)