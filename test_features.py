import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_features():
    session = requests.Session()
    
    # Login
    print("Logging in...")
    login_data = {
        "username": "api_test_user",
        "password": "password123"
    }
    response = session.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if response.status_code != 200:
        print("Login failed")
        return

    # Check new pages
    pages = ["expenses/", "budgets/", "goals/", "insights/"]
    for page in pages:
        resp = session.get(f"{BASE_URL}/{page}")
        print(f"Checking {page}... Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Error content for {page}: {resp.text[:200]}")

    # Test Chatbot Conciseness
    csrf_token = session.cookies.get('csrftoken')
    headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
    
    print("\nTesting Chatbot Conciseness...")
    chat_data = {"message": "How do I save money?"} # General query
    try:
        response = session.post(f"{BASE_URL}/api/chat/send/", json=chat_data, headers=headers)
        print(f"Chat Response: {response.json().get('response')}")
    except Exception as e:
        print(f"Chat Test Failed: {e}")

if __name__ == "__main__":
    test_features()
