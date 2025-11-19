import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_permission_levels():
    print("=== ТЕСТ РАЗНЫХ УРОВНЕЙ ДОСТУПА ===\n")
    
    print("1.СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ С РОЛЬЮ USER")
    user_data = {
        "email": "test_user_role5@example.com",
        "first_name": "Test",
        "last_name": "User", 
        "password": "password123",
        "password_confirm": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
    if response.status_code == 201:
        user_id = response.json().get('user_id')
        print(f"Создан пользователь ID: {user_id}\n")
    else:
        print(f"Ошибка регистрации: {response.json()}")
        return
    
    print("2. ЛОГИН АДМИНА")
    
    admin_login = {
        "email": "admin@example.com",  
        "password": "admin123"         
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=admin_login)
    
    if response.status_code != 200:
        print(f"Ошибка логина админа: {response.json()}")
        return
    
    admin_token = response.json().get('token')
    admin_headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    print(f"Админ залогинен\n")
    
    print("3. НАЗНАЧАЕМ РОЛЬ USER")
    user_role_data = {
        "user": user_id,
        "role": 3 
    }
    
    response = requests.post(f"{BASE_URL}/access/user-roles/", 
                           json=user_role_data, headers=admin_headers)
    print(f"   Статус назначения роли: {response.status_code}")
    
    if response.status_code == 201:
        print(f"Роль назначена: {response.json()}\n")
    else:
        print(f"Ошибка назначения роли: {response.json()}\n")
        return
    
    print("4. ЛОГИН ТЕСТОВОГО ПОЛЬЗОВАТЕЛЯ")
    user_login = {
        "email": "test_user_role@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=user_login)
    user_token = response.json().get('token')
    user_headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json"
    }
    print(f"Пользователь залогинен\n")
    
    print("5. 🧪 ТЕСТ ДОСТУПА USER")
    
    accessible_endpoints = [
        ("Профиль", f"{BASE_URL}/auth/profile/", "GET"),
        ("Товары", f"{BASE_URL}/business/products/", "GET"),
    ]
    
    forbidden_endpoints = [
        ("Управление ролями", f"{BASE_URL}/access/roles/", "GET"),
        ("Управление правилами", f"{BASE_URL}/access/rules/", "GET"),
        ("Все пользователи", f"{BASE_URL}/access/user-roles/", "GET"),
    ]
    
    print("   ДОСТУП РАЗРЕШЕН:")
    for name, url, method in accessible_endpoints:
        if method == "GET":
            response = requests.get(url, headers=user_headers)
        status = response.status_code
        
        if status == 200:
            print(f"- {name}: 200 OK")
        elif status == 403:
            print(f"- {name}: 403 Forbidden (нет прав)")
        else:
            print(f"- {name}: {status}")
    
    print("\n   ДОСТУП ЗАПРЕЩЕН:")
    for name, url, method in forbidden_endpoints:
        if method == "GET":
            response = requests.get(url, headers=user_headers)
        status = response.status_code
        
        if status == 403:
            print(f"- {name}: 403 Forbidden")
        elif status == 200:
            print(f"- {name}: 200 OK (не должно быть доступно!)")
        else:
            print(f"- {name}: {status}")

if __name__ == "__main__":
    test_permission_levels()