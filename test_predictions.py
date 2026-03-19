"""
Sample Test Cases for Hypertension Prediction API
These test cases demonstrate the expected behavior with different health profiles
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

# Test credentials
TEST_USERNAME = "testuser"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "test123456"

def register_user(username, email, password):
    """Register a new user"""
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    return response.json()

def login_user(username, password):
    """Login and get JWT token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": username, "password": password}
    )
    return response.json()

def make_prediction(token, data):
    """Make a prediction"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/predict",
        json=data,
        headers=headers
    )
    return response.json()

# Sample Test Cases
TEST_CASES = [
    {
        "name": "Test Case 1: Young Healthy Person",
        "data": {
            "age": 25,
            "sex": 0,  # Female
            "cp": 0,   # No chest pain
            "systolic": 118,
            "diastolic": 76,
            "cholesterol": 180,
            "fbs": 0,  # Fasting blood sugar normal
            "restecg": 0,  # Normal resting ECG
            "heart_rate": 70,
            "exang": 0,  # No exercise-induced angina
            "oldpeak": 0,  # No ST depression
            "slope": 1,  # Upsloping
            "ca": 0,  # No vessels colored
            "thal": 3,  # Normal thalassemia
            "glucose": 95
        },
        "expected": "HEALTHY (0)"
    },
    {
        "name": "Test Case 2: Middle-aged with High BP",
        "data": {
            "age": 50,
            "sex": 1,  # Male
            "cp": 1,   # Typical angina
            "systolic": 160,
            "diastolic": 100,
            "cholesterol": 260,
            "fbs": 1,  # Elevated fasting blood sugar
            "restecg": 1,  # Abnormal resting ECG
            "heart_rate": 88,
            "exang": 1,  # Exercise-induced angina
            "oldpeak": 2.0,  # ST depression
            "slope": 2,  # Flat slope
            "ca": 2,  # 2 vessels colored
            "thal": 7,  # Abnormal thalassemia
            "glucose": 130
        },
        "expected": "HIGH BP (1)"
    },
    {
        "name": "Test Case 3: Senior with Very High BP",
        "data": {
            "age": 75,
            "sex": 1,  # Male
            "cp": 2,   # Atypical angina
            "systolic": 190,
            "diastolic": 120,
            "cholesterol": 300,
            "fbs": 1,  # Elevated fasting blood sugar
            "restecg": 2,  # LV hypertrophy
            "heart_rate": 95,
            "exang": 1,  # Exercise-induced angina
            "oldpeak": 3.5,  # Significant ST depression
            "slope": 3,  # Downsloping
            "ca": 3,  # 3 vessels colored
            "thal": 7,  # Abnormal thalassemia
            "glucose": 150
        },
        "expected": "HIGH BP (1)"
    },
    {
        "name": "Test Case 4: Middle-aged Moderately Healthy",
        "data": {
            "age": 45,
            "sex": 0,  # Female
            "cp": 0,   # No chest pain
            "systolic": 130,
            "diastolic": 85,
            "cholesterol": 210,
            "fbs": 0,  # Normal fasting blood sugar
            "restecg": 0,  # Normal resting ECG
            "heart_rate": 75,
            "exang": 0,  # No exercise-induced angina
            "oldpeak": 0.5,  # Minimal ST depression
            "slope": 1,  # Upsloping
            "ca": 0,  # No vessels colored
            "thal": 3,  # Normal thalassemia
            "glucose": 105
        },
        "expected": "HEALTHY (0) or HIGH BP (1) - BORDERLINE"
    },
    {
        "name": "Test Case 5: Young with Risk Factors",
        "data": {
            "age": 35,
            "sex": 1,  # Male
            "cp": 1,   # Typical angina
            "systolic": 155,
            "diastolic": 95,
            "cholesterol": 270,
            "fbs": 1,  # Elevated fasting blood sugar
            "restecg": 1,  # Abnormal resting ECG
            "heart_rate": 85,
            "exang": 1,  # Exercise-induced angina
            "oldpeak": 1.5,  # ST depression
            "slope": 2,  # Flat slope
            "ca": 1,  # 1 vessel colored
            "thal": 7,  # Abnormal thalassemia
            "glucose": 125
        },
        "expected": "HIGH BP (1)"
    },
    {
        "name": "Test Case 6: Older but Healthy",
        "data": {
            "age": 65,
            "sex": 0,  # Female
            "cp": 0,   # No chest pain
            "systolic": 125,
            "diastolic": 80,
            "cholesterol": 190,
            "fbs": 0,  # Normal fasting blood sugar
            "restecg": 0,  # Normal resting ECG
            "heart_rate": 68,
            "exang": 0,  # No exercise-induced angina
            "oldpeak": 0,  # No ST depression
            "slope": 1,  # Upsloping
            "ca": 0,  # No vessels colored
            "thal": 3,  # Normal thalassemia
            "glucose": 100
        },
        "expected": "HEALTHY (0)"
    }
]

def run_tests():
    """Run all test cases"""
    print("\n" + "="*70)
    print("HYPERTENSION PREDICTION TEST CASES")
    print("="*70 + "\n")
    
    # Register user
    print("[1/2] Registering test user...")
    reg_result = register_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
    print(f"Status: {reg_result.get('message', 'Unknown')}\n")
    
    # Login
    print("[2/2] Logging in...")
    login_result = login_user(TEST_USERNAME, TEST_PASSWORD)
    if 'access_token' not in login_result:
        print(f"Login failed: {login_result.get('message')}")
        return
    
    token = login_result['access_token']
    print(f"Status: Login successful\n")
    
    # Run test cases
    print("="*70)
    print("RUNNING PREDICTIONS")
    print("="*70 + "\n")
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test Case {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected']}")
        
        result = make_prediction(token, test_case['data'])
        
        if 'error' in result:
            print(f"Status: ERROR - {result['error']}\n")
        else:
            prediction = result.get('prediction', -1)
            probability = result.get('probability', 0) * 100
            
            status = "HEALTHY (0)" if prediction == 0 else "HIGH BP (1)"
            print(f"Prediction: {status}")
            print(f"Confidence: {probability:.1f}%")
            print(f"Status: {result.get('feedback', {}).get('status', 'Unknown')}\n")

if __name__ == "__main__":
    print("\n⏳ Make sure the Flask app is running on http://localhost:5000\n")
    try:
        run_tests()
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease make sure:")
        print("1. Flask app is running: python app.py")
        print("2. Connected to correct URL: http://localhost:5000")
        print("3. Install requests: pip install requests")
