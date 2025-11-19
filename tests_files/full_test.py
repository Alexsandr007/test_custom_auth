import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def full_lifecycle_test():
    print("=== ПОЛНЫЙ ТЕСТ ЖИЗНЕННОГО ЦИКЛА ПОЛЬЗОВАТЕЛЯ ===\n")
    
    print("1. РЕГИСТРАЦИЯ")
    reg_data = {
        "email": "testuser3@example.com",
        "first_name": "Иван",
        "last_name": "Петров",
        "middle_name": "Сергеевич",
        "password": "password123",
        "password_confirm": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=reg_data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.json()}\n")
    
    print("2. ЛОГИН")
    login_data = {
        "email": "testuser3@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        login_response = response.json()
        token = login_response.get('token')
        print(f"Токен получен: {token[:50]}...")  
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"Заголовки: {headers}\n")
        
        print("3. ПРОФИЛЬ")
        response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"Данные: {response.json()}\n")
        else:
            print(f"Ошибка: {response.json()}\n")
        
        print("4. ОБНОВЛЕНИЕ ПРОФИЛЯ")
        update_data = {
            "first_name": "Алексей",
            "last_name": "Сидоров"
        }
        response = requests.put(f"{BASE_URL}/auth/profile/", json=update_data, headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"Обновленные данные: {response.json()}\n")
        else:
            print(f"Ошибка: {response.json()}\n")
        
        print("5. СМЕНА ПАРОЛЯ")
        password_data = {
            "old_password": "password123",
            "new_password": "newpassword456",
            "new_password_confirm": "newpassword456"
        }
        response = requests.put(f"{BASE_URL}/auth/profile/change-password/", json=password_data, headers=headers)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"Ответ: {response.json()}\n")
        else:
            print(f"Ошибка: {response.json()}\n")
        
        print("6. ЛОГАУТ")
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {response.json()}\n")
        
        print("7. УДАЛЕНИЕ АККАУНТА")
        passwords_to_try = ["password123", "newpassword456"]
        
        for password in passwords_to_try:
            login_data = {
                "email": "testuser@example.com",
                "password": password
            }
            response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
            
            if response.status_code == 200:
                new_token = response.json().get('token')
                delete_headers = {
                    "Authorization": f"Bearer {new_token}",
                    "Content-Type": "application/json"
                }
                
                response = requests.delete(f"{BASE_URL}/auth/delete/", headers=delete_headers)
                print(f"Статус удаления: {response.status_code}")
                print(f"Ответ: {response.json()}")
                break
        else:
            print("Не удалось залогиниться для удаления аккаунта")
        
    else:
        print(f"Ошибка логина: {response.json()}\n")
    
    print("=== ТЕСТ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    full_lifecycle_test()