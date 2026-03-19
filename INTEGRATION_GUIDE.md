# Frontend Integration Guide

## 🎯 Overview

This document explains how the Hypertension Prediction System integrates the ML model with a web frontend and authentication system.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Frontend (HTML/CSS/JavaScript)                      │   │
│  │  - Login/Register Interface                          │   │
│  │  - Prediction Dashboard                              │   │
│  │  - Health Feedback Display                           │   │
│  └──────────────────────┬───────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                         │ API Calls
                         │ (JSON/HTTP)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Flask Backend (Python)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication Module                               │   │
│  │  - User Registration                                 │   │
│  │  - Login with JWT Tokens                             │   │
│  │  - Password Hashing                                  │   │
│  └──────────────────┬───────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Prediction Module                                   │   │
│  │  - Receives health data                              │   │
│  │  - Scales features                                   │   │
│  │  - Runs ML model                                     │   │
│  │  - Generates feedback                                │   │
│  └──────────────────┬───────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Machine Learning Model                              │   │
│  │  - Random Forest Classifier                          │   │
│  │  - Pre-trained on hypertension data                  │   │
│  │  - 100 estimators                                    │   │
│  └──────────────────┬───────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 SQLite Database                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Users Table                                         │   │
│  │  - user_id, username, email, password_hash          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Predictions Table                                   │   │
│  │  - prediction_id, user_id, input_data               │   │
│  │  - prediction, probability, timestamp               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 User Flow

### 1. Registration Flow
```
User fills registration form
    ↓
JavaScript validates input
    ↓
POST /api/auth/register
    ↓
Backend validates data
    ↓
Hash password (Werkzeug)
    ↓
Save to users table
    ↓
Return success/error
    ↓
Redirect to login
```

### 2. Authentication Flow
```
User submits login
    ↓
POST /api/auth/login
    ↓
Verify username exists
    ↓
Check password hash
    ↓
Generate JWT token (valid for 30 days)
    ↓
Return token to frontend
    ↓
Store in localStorage
    ↓
Redirect to dashboard
```

### 3. Prediction Flow
```
User enters health metrics
    ↓
Form validation (client-side)
    ↓
POST /api/predict with JWT token
    ↓
Backend verifies token
    ↓
Extract features
    ↓
Apply StandardScaler
    ↓
Run Random Forest model
    ↓
Get prediction & probability
    ↓
Generate personalized feedback
    ↓
Save to predictions table
    ↓
Return result with health tips
    ↓
Display on dashboard with doctor suggestions
```

## 📡 API Communication

### Request Examples

**Login Request:**
```javascript
fetch('/api/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'john_doe',
        password: 'password123'
    })
})
```

**Prediction Request:**
```javascript
fetch('/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({
        age: 45,
        systolic: 140,
        diastolic: 90,
        heart_rate: 72,
        cholesterol: 220,
        glucose: 110
    })
})
```

## 🔐 Security Implementation

### Token-Based Authentication

1. **Registration**: Password is hashed using Werkzeug's `generate_password_hash()`
2. **Login**: Password verified with `check_password_hash()`
3. **JWT Token**: Created using Flask-JWT-Extended with 30-day expiration
4. **Protected Routes**: Endpoints decorated with `@jwt_required()` verify token
5. **Token Storage**: JWT stored in browser's localStorage

### CORS Configuration

```python
CORS(app)  # Enables cross-origin requests for frontend
```

## 🎨 Frontend Features

### Login Page (`index.html`)
- Toggle between sign-up and sign-in forms
- Client-side validation
- Error/success messages
- Responsive design

### Dashboard (`dashboard.html`)
- **Navigation**: Sidebar with tabs (Prediction, History, Resources)
- **Prediction Tab**: 
  - Form for entering health metrics
  - Real-time result display
  - Health tips and doctor recommendations
  - Confidence score display

- **History Tab**: 
  - List of previous predictions
  - Timestamps and results
  - Filter by status (Normal/High)

- **Resources Tab**:
  - Health tips by category (Diet, Exercise, Stress, Lifestyle)
  - Educational content

## 📊 Data Processing Pipeline

```
User Input (6 metrics)
    ↓
Validation (range checks, type checks)
    ↓
Create numpy array [age, systolic, diastolic, HR, cholesterol, glucose]
    ↓
StandardScaler.transform() (normalize using training data statistics)
    ↓
RandomForestClassifier.predict() (get 0 or 1)
    ↓
RandomForestClassifier.predict_proba() (get confidence)
    ↓
Generate feedback based on prediction
    ↓
Return personalized recommendations
```

## 🔧 Configuration

### Key Settings in `app.py`

```python
# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30 * 24 * 60 * 60  # 30 days

# Database
DATABASE = 'hypertension.db'

# Data path
CSV_PATH = r"C:\Users\karun\Downloads\hypertension_data.csv.zip"
```

## 🚀 Deployment Steps

### Local Development
1. Run `python app.py`
2. Access at `http://localhost:5000`

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]
```

### Cloud Deployment (Heroku Example)
```bash
heroku create my-hypertension-app
git push heroku main
heroku open
```

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS errors | Frontend and backend on different ports | Check CORS_ORIGINS in config |
| 401 Unauthorized | Invalid/expired token | Clear localStorage, login again |
| 404 Not Found | Incorrect API endpoint | Verify endpoint paths |
| Model loading fails | Wrong CSV path | Update CSV_PATH in app.py |
| Database locked | Multiple instances running | Restart and delete .db file |

## 📈 Monitoring & Logging

### Add to `app.py` for production logging:
```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
app.logger.info('Application started')
```

## 🔄 Updating the Model

To retrain with new data:

1. Replace `hypertension_data.csv.zip` with new dataset
2. Update feature names in prediction form if changed
3. Restart Flask application
4. Clear predictions table if schema changes:
   ```python
   cursor.execute('DELETE FROM predictions')
   ```

## 📞 Maintenance

### Regular Tasks
- Monitor disk usage (database file grows with predictions)
- Backup user data regularly
- Review API logs for errors
- Update dependencies quarterly
- Test user feedback reports

### Monthly Tasks
- Clear old predictions (optional, based on privacy policy)
- Verify model accuracy on new data
- Update health tips/resources
- Security review of token handling

---

**Next Steps:**
1. Follow SETUP_GUIDE.md for installation
2. Run the application with `run.bat` (Windows) or `run.sh` (Linux/Mac)
3. Create test account and verify all features
4. Customize health tips and doctor recommendations as needed
