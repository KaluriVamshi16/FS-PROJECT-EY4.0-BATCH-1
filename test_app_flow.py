import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_flow():
    session = requests.Session()
    
    # 1. Register
    print("Testing Registration...")
    reg_data = {
        "username": "api_test_user",
        "email": "api_test@example.com",
        "password": "password123"
    }
    # Clean up first if exists (not possible via API easily without admin, so assume fresh or handle error)
    
    try:
        response = session.post(f"{BASE_URL}/api/auth/register/", json=reg_data)
        print(f"Register Status: {response.status_code}")
        print(f"Register Response: {response.text}")
    except Exception as e:
        print(f"Register Failed: {e}")

    # 2. Login
    print("\nTesting Login...")
    login_data = {
        "username": "api_test_user",
        "password": "password123"
    }
    response = session.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    print(f"Login Status: {response.status_code}")
    # print(f"Login Response: {response.text}") # Might be verbose

    if response.status_code == 200:
        # 3. Get Dashboard Data
        print("\nTesting Dashboard Data...")
        response = session.get(f"{BASE_URL}/dashboard/api/data/")
        print(f"Dashboard Data Status: {response.status_code}")
        print(f"Dashboard Data: {response.json()}")

        # 4. Chat Message (with CSRF token handling if needed, but session auth usually checks CSRF)
        # DRF SessionAuth enforces CSRF. We need to get the token.
        # It's in the cookie 'csrftoken'
        csrf_token = session.cookies.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
        
        print("\nTesting Chat...")
        chat_data = {"message": "Hello FinSight"}
        response = session.post(f"{BASE_URL}/api/chat/send/", json=chat_data, headers=headers)
        print(f"Chat Status: {response.status_code}")
        print(f"Chat Response: {response.text}")

        # 5. Add Expense via Chat (Mocked if no Groq Key, but let's try)
        # Assuming the fallback response is text, it won't add expense.
        # But if we had logic to parse "I spent 100", let's try.
        # groq_utils.py needs key. If missing, it returns error message.
    else:
        print("Login failed, skipping authenticated tests.")

if __name__ == "__main__":
    test_flow()
