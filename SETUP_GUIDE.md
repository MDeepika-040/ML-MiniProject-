# Hypertension Prediction System with Authentication

A full-stack web application for hypertension prediction with user authentication, featuring a machine learning model trained on hypertension data.

## 🎯 Features

✅ **User Authentication**
- Secure sign-up and sign-in system
- JWT token-based authentication
- SQLite database for user management

📊 **Prediction System**
- ML-powered hypertension prediction
- Personalized health feedback
- Doctor recommendations based on location
- Confidence scores for predictions

📈 **Dashboard**
- Prediction history tracking
- Health tips and resources
- Interactive prediction interface

## 📁 Project Structure

```
Hypertension-main/
├── app.py                      # Flask backend application
├── hypertension.ipynb          # Original ML model notebook
├── hypertension_data.csv.zip   # Training data
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html             # Login/Register page
│   └── dashboard.html         # Main dashboard
├── static/
│   ├── style.css              # Styling
│   ├── auth.js                # Authentication logic
│   └── dashboard.js           # Dashboard functionality
└── README.md                  # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Windows/Mac/Linux

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Application

Open `app.py` and update the CSV file path if necessary:
```python
csv_path = r"C:\Users\karun\Downloads\hypertension_data.csv.zip"  # Change if different
```

Also change the JWT secret key (important for production):
```python
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this'
```

### 3. Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

### 4. Access the Application

1. Open your browser and go to `http://localhost:5000`
2. Register a new account
3. Sign in with your credentials
4. Use the dashboard to make predictions

## 📖 API Endpoints

### Authentication

**Register User**
```
POST /api/auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
}
```

**Login**
```
POST /api/auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "secure_password"
}
```

### Predictions

**Make Prediction** (Requires JWT Token)
```
POST /api/predict
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
    "age": 45,
    "systolic": 140,
    "diastolic": 90,
    "heart_rate": 72,
    "cholesterol": 220,
    "glucose": 110
}
```

**Get Prediction History** (Requires JWT Token)
```
GET /api/prediction-history
Authorization: Bearer <JWT_TOKEN>
```

## 🎓 How It Works

1. **User Registration & Login**: Users create accounts and log in securely
2. **Data Input**: Users enter their health metrics through the dashboard
3. **Model Prediction**: The trained ML model predicts hypertension risk
4. **Personalized Feedback**: Users receive:
   - Health status (Normal/High BP)
   - Specific health tips
   - Recommended doctors nearby
   - Fitness and lifestyle recommendations
5. **History Tracking**: All predictions are saved and can be reviewed

## 🏥 Health Information Collected

- **Age**: Patient's age in years
- **Systolic BP**: Upper blood pressure reading (mmHg)
- **Diastolic BP**: Lower blood pressure reading (mmHg)
- **Heart Rate**: Pulse (beats per minute)
- **Cholesterol**: Total cholesterol level (mg/dL)
- **Glucose**: Blood glucose level (mg/dL)

## 💡 Prediction Output

For **High BP (Hypertension)** cases:
- Alert status: ⚠️ HIGH BLOOD PRESSURE DETECTED
- Urgent action: Contact healthcare consultant immediately
- Tailored health tips for managing hypertension
- List of specialized cardiologists nearby

For **Normal/Healthy** cases:
- Confirmation status: ✅ HEALTHY BLOOD PRESSURE
- Encouragement message with health maintenance tips
- General practitioners and preventive medicine specialists

## 🔒 Security Features

- Password hashing using Werkzeug
- JWT token-based authentication
- Protected API endpoints with @jwt_required decorator
- CORS enabled for cross-origin requests
- Database constraints for data integrity

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Predictions Table
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    input_data TEXT NOT NULL,
    prediction INTEGER NOT NULL,
    probability REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

## 🎨 Tech Stack

- **Backend**: Flask, Flask-JWT-Extended, Flask-CORS
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite
- **ML Model**: scikit-learn Random Forest Classifier
- **Data Processing**: pandas, numpy

## 🐛 Troubleshooting

**Issue**: "Failed to load model" error
- Solution: Ensure the CSV file path in `app.py` is correct

**Issue**: "Module not found" errors
- Solution: Run `pip install -r requirements.txt` again

**Issue**: Port 5000 already in use
- Solution: Change port in `app.py`: `app.run(debug=True, port=5001)`

**Issue**: Database locked error
- Solution: Close any other instances of the app and delete `hypertension.db` to reset

## 📝 Sample Test Users

You can register your own accounts, or the database will be created automatically on first run.

## 🔐 Production Deployment

Before deploying to production:

1. Change JWT_SECRET_KEY to a strong random value
2. Set `debug=False` in app.py
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up proper database backups
5. Enable HTTPS/SSL certificates
6. Use environment variables for sensitive data
7. Implement rate limiting on API endpoints

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📞 Support & Contact

For issues or questions, please refer to the original notebook for model details.

## 📄 License

This project is provided as-is for educational and health monitoring purposes.

---

**Note**: This application is for educational purposes. Medical predictions should always be verified by healthcare professionals.
