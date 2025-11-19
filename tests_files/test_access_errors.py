import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def safe_json_response(response):
    try:
        return response.json()
    except:
        return {"raw_text": response.text[:200]}

def test_access_errors():
    print("=== ТЕСТ ОШИБОК ДОСТУПА ===\n")
    
    print("1. СОЗДАЕМ ОБЫЧНОГО ПОЛЬЗОВАТЕЛЯ")
    reg_data = {
        "email": "regular_user@example.com",
        "first_name": "Обычный",
        "last_name": "Пользователь", 
        "password": "password123",
        "password_confirm": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=reg_data)
    print(f"Статус: {response.status_code}\n")
    
    print("2. ЛОГИН ОБЫЧНОГО ПОЛЬЗОВАТЕЛЯ")
    login_data = {
        "email": "regular_user@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    regular_token = response.json().get('token')
    print(f"Статус: {response.status_code}")
    print(f"Токен получен: {regular_token[:30]}...\n")
    
    regular_headers = {
        "Authorization": f"Bearer {regular_token}",
        "Content-Type": "application/json"
    }
    
    print("3. ТЕСТ 401 UNAUTHORIZED (без токена)")
    response = requests.get(f"{BASE_URL}/auth/profile/")
    print(f"Статус: {response.status_code} (ожидаем 401)")
    print(f"Ответ: {safe_json_response(response)}\n")
    
    print("4. ТЕСТ ДОСТУПА К РАЗНЫМ ENDPOINTS")
    
    endpoints_to_test = [
        ("Профиль (должен быть доступен)", "/auth/profile/", 200),
        ("Товары (бизнес-модуль)", "/business/products/", "?"),
        ("Заказы (бизнес-модуль)", "/business/orders/", "?"),
        ("Управление ролями", "/access/roles/", 403),
        ("Управление правилами", "/access/rules/", 403),
        ("Управление пользователь-ролями", "/access/user-roles/", 403),
    ]
    
    for name, endpoint in endpoints_to_test:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=regular_headers)
        actual_status = response.status_code
        
        
        print(f"{name}:")
        print(f"Статус: {actual_status}")
        
        if actual_status == 200:
            data = safe_json_response(response)
            if isinstance(data, list):
                print(f"Данные: список из {len(data)} элементов")
            else:
                print(f"Данные: {list(data.keys()) if isinstance(data, dict) else 'available'}")
        elif actual_status == 403:
            print(f"Ответ: {safe_json_response(response)}")
        elif actual_status == 404:
            print(f"Endpoint не найден! Нужно настроить URL")
        elif actual_status == 401:
            print(f"Ответ: {safe_json_response(response)}")
        else:
            print(f"Ответ: {safe_json_response(response)}")
        print()

if __name__ == "__main__":
    test_access_errors()