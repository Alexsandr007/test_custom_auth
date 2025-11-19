import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def final_test():
    print("=== ФИНАЛЬНЫЙ ТЕСТ АУТЕНТИФИКАЦИИ ===\n")
    
    print("1. 🔐 ЛОГИН")
    login_data = {
        "email": "testuser3@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"   Статус: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        user_data = data.get('user')
        print(f"Токен получен")
        print(f"Пользователь: {user_data['email']}\n")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("2. ПРОФИЛЬ С ТОКЕНОМ")
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            profile_data = response.json()
            print(f"Профиль получен:")
            print(f"ID: {profile_data['id']}")
            print(f"Email: {profile_data['email']}")
            print(f"Имя: {profile_data['first_name']} {profile_data['last_name']}")
        else:
            print(f"Ошибка: {response.json()}")
        print()
        
        print("3. ОБНОВЛЕНИЕ ПРОФИЛЯ")
        update_data = {
            "first_name": "Алексей",
            "last_name": "Сидоров"
        }
        response = requests.put(f"{BASE_URL}/auth/profile/", json=update_data, headers=headers)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            updated_data = response.json()
            print(f"Профиль обновлен:")
            print(f"Новое имя: {updated_data['first_name']} {updated_data['last_name']}")
        else:
            print(f"Ошибка: {response.json()}")
        print()
        
        print("4. СМЕНА ПАРОЛЯ")
        password_data = {
            "old_password": "password123",
            "new_password": "newpassword456",
            "new_password_confirm": "newpassword456"
        }
        response = requests.put(f"{BASE_URL}/auth/profile/change-password/", json=password_data, headers=headers)
        print(f"   Статус: {response.status_code}")
        
        if response.status_code == 200:
            print(f"{response.json()['message']}")
        else:
            print(f"Ошибка: {response.json()}")
        print()
        
        print("5. ЛОГАУТ")
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"{response.json()['message']}\n")
        
        print("6. УДАЛЕНИЕ АККАУНТА")
        new_login_data = {
            "email": "testuser3@example.com",
            "password": "newpassword456"
        }
        response = requests.post(f"{BASE_URL}/auth/login/", json=new_login_data)
        
        if response.status_code == 200:
            new_token = response.json().get('token')
            delete_headers = {
                "Authorization": f"Bearer {new_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.delete(f"{BASE_URL}/auth/delete/", headers=delete_headers)
            print(f"Статус: {response.status_code}")
            
            if response.status_code == 200:
                print(f"{response.json()['message']}")
                
                print("\n7. ПРОВЕРКА ЧТО АККАУНТ УДАЛЕН")
                time.sleep(1)
                
                response = requests.post(f"{BASE_URL}/auth/login/", json=new_login_data)
                print(f"   Статус: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"Аккаунт действительно удален - логин невозможен")
                else:
                    print(f"Аккаунт все еще доступен")
            else:
                print(f"Ошибка удаления: {response.json()}")
        else:
            print(f"Не удалось залогиниться для удаления")
    
    print("\n=== ТЕСТ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    final_test()