# Quick Start Testing Guide

## 🚀 Option 1: Test Using the Web Form (Easiest)

### Step 1: Start the Application
```bash
python app.py
```
You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
✓ Model trained successfully! Accuracy: 1.0000
```

### Step 2: Open in Browser
Navigate to: **http://localhost:5000**

### Step 3: Create Account & Login
1. Click "Sign Up"
2. Enter credentials:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test123`
3. Click "Sign In"
4. Enter username and password

### Step 4: Fill the Prediction Form with Test Cases

#### Test Case 1: **HEALTHY (Expected: ✅ HEALTHY BLOOD PRESSURE)**
Fill the form with:
- **Age:** 28
- **Sex:** Female (0)
- **Chest Pain Type:** Asymptomatic (3)
- **Systolic BP:** 120 mmHg
- **Diastolic BP:** 80 mmHg
- **Heart Rate:** 70 bpm
- **Cholesterol:** 180 mg/dL
- **Glucose:** 95 mg/dL
- **Fasting Blood Sugar:** No (0)
- **Resting ECG:** Normal (0)
- **Exercise-Induced Angina:** No (0)
- **ST Depression:** 0.0
- **ST Segment Slope:** Upsloping (1)
- **Major Vessels:** 0
- **Thalassemia:** Normal (3)

**Click "Get Prediction"** → Should show ✅ **HEALTHY BLOOD PRESSURE**

---

#### Test Case 2: **HIGH BP (Expected: ⚠️ HIGH BLOOD PRESSURE)**
Fill the form with:
- **Age:** 55
- **Sex:** Male (1)
- **Chest Pain Type:** Atypical Angina (1)
- **Systolic BP:** 165 mmHg
- **Diastolic BP:** 105 mmHg
- **Heart Rate:** 88 bpm
- **Cholesterol:** 270 mg/dL
- **Glucose:** 135 mg/dL
- **Fasting Blood Sugar:** Yes (1)
- **Resting ECG:** ST-T Abnormality (1)
- **Exercise-Induced Angina:** Yes (1)
- **ST Depression:** 2.0
- **ST Segment Slope:** Flat (2)
- **Major Vessels:** 2
- **Thalassemia:** Reversible Defect (7)

**Click "Get Prediction"** → Should show ⚠️ **HIGH BLOOD PRESSURE DETECTED** + doctors list

---

#### Test Case 3: **CRITICAL (Expected: ⚠️ HIGH BLOOD PRESSURE)**
Fill the form with:
- **Age:** 72
- **Sex:** Male (1)
- **Chest Pain Type:** Non-Anginal Pain (2)
- **Systolic BP:** 185 mmHg
- **Diastolic BP:** 115 mmHg
- **Heart Rate:** 92 bpm
- **Cholesterol:** 295 mg/dL
- **Glucose:** 155 mg/dL
- **Fasting Blood Sugar:** Yes (1)
- **Resting ECG:** LV Hypertrophy (2)
- **Exercise-Induced Angina:** Yes (1)
- **ST Depression:** 3.0
- **ST Segment Slope:** Downsloping (3)
- **Major Vessels:** 3
- **Thalassemia:** Reversible Defect (7)

**Click "Get Prediction"** → Should show ⚠️ **HIGH BLOOD PRESSURE DETECTED** + doctors list

---

## 🚀 Option 2: Test Using API with Python Script

### Step 1: Ensure Flask is Running
```bash
python app.py
```

### Step 2: Run Tests
```bash
python test_predictions.py
```

**Expected Output:**
All 6 tests should run and show mixed results:
- ✅ Tests 1, 5: Should show Prediction = 0 (HEALTHY)
- ⚠️ Tests 2, 3, 4, 6: Should show Prediction = 1 (HIGH BP)

### Step 3: Check Debug Logs
Look at the Flask terminal for this output pattern:
```
--- PREDICTION DEBUG ---
Raw features: age=28, sex=0, cp=3, systolic=120, ...
Scaled features: [0.12, -0.45, 1.23, -0.89, ...]
Probabilities: Class 0=0.9872, Class 1=0.0128
Prediction: 0
---
```

---

## 🚀 Option 3: Test Using cURL Commands

### Prerequisites
```bash
# Get the access token first
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"curluser","email":"curl@test.com","password":"test123"}'

curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"curluser","password":"test123"}'
```
Copy the `access_token` from response.

### Test Healthy Case
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "age": 28, "sex": 0, "cp": 3, "systolic": 120, "diastolic": 80,
    "cholesterol": 180, "fbs": 0, "restecg": 0, "heart_rate": 70,
    "exang": 0, "oldpeak": 0, "slope": 1, "ca": 0, "thal": 3, "glucose": 95
  }'
```

Expected:
```json
{
  "prediction": 0,
  "probability": 0.987,
  "feedback": {
    "status": "HEALTHY BLOOD PRESSURE",
    "severity": "NORMAL",
    "doctor_note": "",
    "tips": ["Maintain your current lifestyle", ...],
    "doctors": []
  }
}
```

### Test High BP Case
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "age": 55, "sex": 1, "cp": 1, "systolic": 165, "diastolic": 105,
    "cholesterol": 270, "fbs": 1, "restecg": 1, "heart_rate": 88,
    "exang": 1, "oldpeak": 2, "slope": 2, "ca": 2, "thal": 7, "glucose": 135
  }'
```

Expected:
```json
{
  "prediction": 1,
  "probability": 0.945,
  "feedback": {
    "status": "HIGH BLOOD PRESSURE DETECTED",
    "severity": "HIGH",
    "doctor_note": "Please consult a cardiologist immediately",
    "tips": [...],
    "doctors": [
      {"name": "Dr. Sarah Johnson", "specialty": "Cardiologist", ...},
      {"name": "Dr. James Wilson", "specialty": "Internal Medicine", ...}
    ]
  }
}
```

---

## ✅ Expected Results Summary

| Test Case | Age | Systolic | Expected | Doctor List |
|-----------|-----|----------|----------|-------------|
| 1. Young Healthy | 28 | 120 | ✅ 0 | No doctors |
| 2. Middle Age High | 55 | 165 | ⚠️ 1 | Show doctors |
| 3. Elderly Critical | 72 | 185 | ⚠️ 1 | Show doctors |
| 4. Young at Risk | 38 | 158 | ⚠️ 1 | Show doctors |
| 5. Healthy Older | 68 | 128 | ✅ 0 | No doctors |
| 6. Borderline | 48 | 145 | ? 0 or 1 | Maybe doctors |

---

## 🐛 Troubleshooting

### If all predictions show HEALTHY:
1. **Check model training:** Terminal should show `✓ Model trained successfully! Accuracy: 1.0000`
2. **Check debug output:** Look for `--- PREDICTION DEBUG ---` section in Flask terminal
3. **Verify features:** Compare form values with test cases
4. **Restart app:** `python app.py`

### If you see import errors:
```bash
pip install -r requirements.txt
# Or individually:
pip install flask flask-cors flask-jwt-extended scikit-learn pandas numpy
```

### If database errors occur:
```bash
# Delete old database
rm predictions.db

# Restart app (will recreate database)
python app.py
```

### If location permission issues:
- Click the location icon in browser address bar
- Select "Allow" when prompted
- The status will change to "✓ Location enabled"

---

## 📊 Monitoring Predictions

Watch the Flask terminal to see:
1. Raw feature extraction
2. Feature scaling values
3. Both class probabilities
4. Final prediction

Example debug output:
```
--- PREDICTION DEBUG ---
Raw features: age=28, sex=0, cp=3, systolic=120, diastolic=80, chol=180, fbs=0, restecg=0, thalach=70, exang=0, oldpeak=0.0, slope=1, ca=0, thal=3
Scaled (first 5): [-0.76  -0.56   1.33  -1.23  -0.87]
Probabilities: Class 0 = 0.9872, Class 1 = 0.0128
Prediction: 0 (HEALTHY)
---
```

---

## 🎯 What to Verify

✅ Predictions vary based on input values (not all the same)  
✅ Higher systolic BP → More likely prediction 1  
✅ Doctors shown only for HIGH BP cases  
✅ Location status updates in dashboard header  
✅ History tab shows past predictions  
✅ Debug logs show feature flow in Flask terminal  

If all these are working, the model integration is successful! 🎉
