import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8001"

def test_features():
    session = requests.Session()
    
    with open("feature_verification.log", "w", encoding="utf-8") as f:
        # Login
        f.write("Logging in...\n")
        login_data = {
            "username": "api_test_user",
            "password": "password123"
        }
        try:
            response = session.post(f"{BASE_URL}/api/auth/login/", json=login_data)
            f.write(f"Login Status: {response.status_code}\n")
        except Exception as e:
            f.write(f"Login Exception: {e}\n")
            return

        # Check new pages
        pages = ["expenses/", "budgets/", "goals/", "insights/"]
        for page in pages:
            try:
                resp = session.get(f"{BASE_URL}/{page}")
                f.write(f"Checking {page}... Status: {resp.status_code}\n")
                if resp.status_code == 200:
                    if "FinSight" in resp.text:
                         f.write(f"  -> Content seems valid (found Title).\n")
                    else:
                         f.write(f"  -> Warning: Title not found in content.\n")
                else:
                    f.write(f"  -> Error content: {resp.text[:100]}\n")
            except Exception as e:
                f.write(f"Exception checking {page}: {e}\n")

        # Test Chatbot Conciseness
        csrf_token = session.cookies.get('csrftoken')
        headers = {'X-CSRFToken': csrf_token} if csrf_token else {}
        
        f.write("\nTesting Chatbot Conciseness...\n")
        chat_data = {"message": "How do I save money?"} # General query
        try:
            response = session.post(f"{BASE_URL}/api/chat/send/", json=chat_data, headers=headers)
            f.write(f"Chat Response Status: {response.status_code}\n")
            if response.status_code == 200:
                answer = response.json().get('response', '')
                f.write(f"Chat Answer: {answer}\n")
                if "\n" in answer or "-" in answer or "•" in answer:
                    f.write("  -> Format appears structured/bulleted.\n")
            else:
                f.write(f"  -> Chat Error: {response.text}\n")
        except Exception as e:
            f.write(f"Chat Test Failed: {e}\n")

if __name__ == "__main__":
    test_features()
