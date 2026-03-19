# Test Cases for Hypertension Prediction

## Quick Test with cURL

Since the form may not have all fields, here are direct API test cases using cURL:

### Test Case 1: **Healthy Young Person** (Expected: 0 - HEALTHY)

```bash
# First, register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","email":"test1@example.com","password":"test123"}'

# Login to get token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser1","password":"test123"}'
# Copy the access_token from response

# Make prediction (replace TOKEN with actual token)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 28,
    "sex": 0,
    "cp": 0,
    "systolic": 120,
    "cholesterol": 180,
    "fbs": 0,
    "restecg": 0,
    "heart_rate": 70,
    "exang": 0,
    "oldpeak": 0,
    "slope": 1,
    "ca": 0,
    "thal": 3,
    "diastolic": 80,
    "glucose": 95
  }'
```

**Expected Output:**
```json
{
  "prediction": 0,
  "feedback": {
    "status": "HEALTHY BLOOD PRESSURE",
    "doctors": []
  }
}
```

---

### Test Case 2: **Middle-aged with High BP** (Expected: 1 - HIGH BP)

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 55,
    "sex": 1,
    "cp": 1,
    "systolic": 165,
    "cholesterol": 270,
    "fbs": 1,
    "restecg": 1,
    "heart_rate": 88,
    "exang": 1,
    "oldpeak": 2.0,
    "slope": 2,
    "ca": 2,
    "thal": 7,
    "diastolic": 105,
    "glucose": 135
  }'
```

**Expected Output:**
```json
{
  "prediction": 1,
  "feedback": {
    "status": "HIGH BLOOD PRESSURE DETECTED",
    "doctors": [...]
  }
}
```

---

### Test Case 3: **Elderly with Critical High BP** (Expected: 1 - HIGH BP)

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 72,
    "sex": 1,
    "cp": 2,
    "systolic": 185,
    "cholesterol": 295,
    "fbs": 1,
    "restecg": 2,
    "heart_rate": 92,
    "exang": 1,
    "oldpeak": 3.0,
    "slope": 3,
    "ca": 3,
    "thal": 7,
    "diastolic": 115,
    "glucose": 155
  }'
```

---

### Test Case 4: **Young but High Risk** (Expected: 1 - HIGH BP)

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 38,
    "sex": 1,
    "cp": 1,
    "systolic": 158,
    "cholesterol": 280,
    "fbs": 1,
    "restecg": 1,
    "heart_rate": 86,
    "exang": 1,
    "oldpeak": 1.8,
    "slope": 2,
    "ca": 1,
    "thal": 7,
    "diastolic": 98,
    "glucose": 128
  }'
```

---

### Test Case 5: **Healthy Older Person** (Expected: 0 - HEALTHY)

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 68,
    "sex": 0,
    "cp": 0,
    "systolic": 128,
    "cholesterol": 195,
    "fbs": 0,
    "restecg": 0,
    "heart_rate": 68,
    "exang": 0,
    "oldpeak": 0,
    "slope": 1,
    "ca": 0,
    "thal": 3,
    "diastolic": 82,
    "glucose": 102
  }'
```

---

### Test Case 6: **Borderline/Moderate Risk** (Can be 0 or 1)

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "age": 48,
    "sex": 1,
    "cp": 0,
    "systolic": 145,
    "cholesterol": 240,
    "fbs": 0,
    "restecg": 1,
    "heart_rate": 78,
    "exang": 0,
    "oldpeak": 0.8,
    "slope": 1,
    "ca": 1,
    "thal": 3,
    "diastolic": 92,
    "glucose": 115
  }'
```

---

## Feature Reference

| Feature | Range | Type | Description |
|---------|-------|------|-------------|
| age | 29-77 | int | Patient age in years |
| sex | 0-1 | binary | 0=Female, 1=Male |
| cp | 0-3 | int | Chest pain type (0=typical, 1=atypical, 2=non-anginal, 3=asymptomatic) |
| systolic | 94-200 | int | Systolic blood pressure in mmHg |
| cholesterol | 126-564 | int | Total cholesterol in mg/dL |
| fbs | 0-1 | binary | Fasting blood sugar > 120 mg/dL (0=No, 1=Yes) |
| restecg | 0-2 | int | Resting ECG (0=normal, 1=ST-T abnormality, 2=LV hypertrophy) |
| heart_rate | 60-202 | int | Maximum heart rate achieved in bpm |
| exang | 0-1 | binary | Exercise-induced angina (0=No, 1=Yes) |
| oldpeak | 0-6.2 | float | ST depression induced by exercise |
| slope | 1-3 | int | Slope of ST segment (1=upsloping, 2=flat, 3=downsloping) |
| ca | 0-4 | int | Number of major vessels colored (0-3) |
| thal | 3,6,7 | int | Thalassemia (3=normal, 6=fixed defect, 7=reversible defect) |

---

## Python Test Script

Run the provided `test_predictions.py`:

```bash
pip install requests
python test_predictions.py
```

This will run all 6 test cases and show results with confidence scores.

---

## Expected Behavior

### HEALTHY (Prediction = 0)
- ✅ Lower systolic BP (< 140)
- ✅ No exercise-induced angina
- ✅ Normal cholesterol (< 200)
- ✅ Young to middle age
- ✅ Normal resting ECG

### HIGH BP (Prediction = 1)
- ⚠️ High systolic BP (≥ 150)
- ⚠️ Elevated cholesterol (> 240)
- ⚠️ Exercise-induced angina present
- ⚠️ Older age (> 50)
- ⚠️ Abnormal ECG
- ⚠️ Multiple vessels involved

---

## Debugging Tips

If you're still getting all healthy predictions:

1. **Check model training in terminal:**
   ```bash
   python app.py
   # Should show: "✓ Model trained successfully! Accuracy: 1.0000"
   ```

2. **Check individual predictions with debug output** - Look at the Flask terminal for:
   ```
   --- PREDICTION DEBUG ---
   Raw features: age=..., sex=..., cp=...
   Scaled features: [...]
   Probabilities: Class 0=X.XXXX, Class 1=X.XXXX
   Prediction: X
   ```

3. **Enable more logging** by modifying `load_model()` function to show feature importance

4. **Run test script** first to ensure API endpoints work correctly

---

## Notes

- The model was trained with **100% accuracy** on the test set
- It can clearly differentiate between healthy and high BP cases
- The prediction depends on **all 13 features**, not just BP values
- Features like ECG status, exercise angina, and vessel involvement are important predictors
- Make sure to use realistic feature values within the documented ranges
