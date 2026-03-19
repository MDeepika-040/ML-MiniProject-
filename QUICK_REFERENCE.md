# 🚀 Quick Reference Card

## ⚡ Quick Start (60 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
python app.py

# 3. Open in browser
# http://localhost:5000
```

## 📋 Project Structure

```
📁 Hypertension-main/
├── 📄 app.py                 ← Flask backend (START HERE)
├── 📄 config.py              ← Configuration settings
├── 📄 requirements.txt        ← Python packages
├── 📄 hypertension.ipynb      ← Original ML model
├── 📁 templates/
│   ├── index.html            ← Login/Register page
│   └── dashboard.html        ← Main dashboard
├── 📁 static/
│   ├── style.css             ← Styling
│   ├── auth.js               ← Authentication logic
│   └── dashboard.js          ← Dashboard functionality
├── 📄 run.bat                ← Windows quick start
├── 📄 run.sh                 ← Linux/Mac quick start
├── 📖 SETUP_GUIDE.md         ← Detailed setup
├── 📖 INTEGRATION_GUIDE.md    ← Architecture & integration
├── 📖 TESTING_GUIDE.md        ← Testing procedures
└── 📖 README.md              ← Project overview
```

## 🔑 Key Features

| Feature | Details |
|---------|---------|
| **Authentication** | Sign up, login, JWT tokens (30 day expiry) |
| **Prediction** | Enter 6 health metrics, get instant feedback |
| **Feedback** | Health tips, doctor recommendations, confidence score |
| **History** | Track all predictions with timestamps |
| **Resources** | Diet, exercise, stress, lifestyle tips |
| **Database** | SQLite with users and predictions tables |
| **Security** | Password hashing, CORS enabled, JWT protected |

## 🎯 API Endpoints

```javascript
// Authentication
POST   /api/auth/register         // Register new user
POST   /api/auth/login            // Login (returns JWT token)

// Predictions (require JWT token)
POST   /api/predict               // Make prediction
GET    /api/prediction-history    // Get user's predictions

// Web Pages
GET    /                          // Home/login page
GET    /dashboard                 // Main dashboard
```

## 📊 Health Metrics Required

| Input | Range | Example |
|-------|-------|---------|
| Age | 1-150 | 45 |
| Systolic BP | 60-250 | 140 |
| Diastolic BP | 40-150 | 90 |
| Heart Rate | 30-200 | 72 |
| Cholesterol | 0-400 | 220 |
| Glucose | 0-500 | 110 |

## 🎨 Prediction Results

### Normal/Healthy ✅
- Status: "HEALTHY BLOOD PRESSURE"
- Action: Keep up health habits
- Tips: Fitness & prevention focused
- Doctors: General practitioners

### High BP ⚠️
- Status: "HIGH BLOOD PRESSURE DETECTED"
- Action: Contact consultant immediately
- Tips: Hypertension management
- Doctors: Cardiologists & specialists

## 💾 Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    created_at TIMESTAMP
)

-- Predictions Table
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    input_data TEXT,
    prediction INTEGER (0=normal, 1=high),
    probability REAL,
    created_at TIMESTAMP
)
```

## 🔐 Security Checklist

- [x] Password hashing (Werkzeug)
- [x] JWT token authentication
- [x] Protected API endpoints
- [x] CORS enabled
- [x] Database constraints
- [ ] ⚠️ Change JWT_SECRET_KEY in config.py
- [ ] ⚠️ Set DEBUG=False for production
- [ ] ⚠️ Use environment variables for secrets

## 🐛 Common Commands

```bash
# Install packages
pip install -r requirements.txt

# Run app
python app.py

# Add new package
pip install flask-newfeature

# Update requirements
pip freeze > requirements.txt

# Reset database
# Delete hypertension.db (it will recreate on next run)

# Run on different port
# Edit app.py: app.run(debug=True, port=5001)
```

## 📱 Frontend Login Flow

```
1. User Registration → Validate → Hash password → Save to DB
                    ↓
2. User Login → Validate → Check password → Create JWT
              ↓
3. Store token → localStorage
              ↓
4. Access dashboard → Send token with requests
                    ↓
5. Logout → Clear localStorage

```

## 📊 Prediction ML Model

```
Algorithm: Random Forest Classifier
Estimators: 100 trees
Training Data: hypertension_data.csv.zip
Features: 6 (age, systolic, diastolic, HR, cholesterol, glucose)
Output: Binary (0 = Normal, 1 = High BP)
Confidence: Probability score (0.0 - 1.0)
Data Scaling: StandardScaler normalization
```

## 🚀 Deployment Checklist

### Before Going Live
- [ ] Update JWT_SECRET_KEY
- [ ] Change DEBUG to False
- [ ] Test all features
- [ ] Set up database backups
- [ ] Configure CORS properly
- [ ] Use HTTPS/SSL
- [ ] Set up monitoring/logging
- [ ] Document for team
- [ ] Create admin account
- [ ] Test on production database

### Deployment Options
- **Local**: `python app.py`
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- **Docker**: See INTEGRATION_GUIDE.md
- **Heroku**: Connect Git repo and deploy
- **AWS**: Lambda + RDS + CloudFront

## 📞 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Change port in app.py or kill process |
| Module not found | Run `pip install -r requirements.txt` |
| CSV not found | Update CSV_PATH in app.py |
| Database locked | Delete hypertension.db and restart |
| 401 Unauthorized | Login again, token may be expired |
| CORS errors | Check frontend URL in CORS_ORIGINS |
| 404 Not Found | Verify API endpoint path is correct |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| SETUP_GUIDE.md | Installation & configuration |
| INTEGRATION_GUIDE.md | Full architecture & integration |
| TESTING_GUIDE.md | Complete testing procedures |
| config.py | Configuration management |

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **JWT**: https://tools.ietf.org/html/rfc7519
- **scikit-learn**: https://scikit-learn.org/
- **SQLite**: https://www.sqlite.org/
- **JavaScript Fetch API**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

## 💡 Pro Tips

1. Use DevTools Console to check localStorage: `localStorage.getItem('access_token')`
2. Test API endpoints with Postman or curl
3. Monitor predictions to improve model accuracy
4. Backup database regularly
5. Update health tips based on latest medical guidelines
6. Log all API requests for debugging
7. Set up email notifications for high BP predictions
8. Consider adding user profile settings

## 🎯 Next Steps

1. ✅ Run `python app.py`
2. ✅ Register new account
3. ✅ Test prediction
4. ✅ Review history
5. ✅ Read INTEGRATION_GUIDE.md for architecture
6. ✅ Run TESTING_GUIDE.md procedures
7. ✅ Customize for your needs
8. ✅ Deploy to production

---

**Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Production Ready

🎉 **You're all set! Happy coding!** 🎉
