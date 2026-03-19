from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-this'  # Change this in production
app.config['JSON_SORT_KEYS'] = False

# Initialize JWT
jwt = JWTManager(app)
CORS(app)

# Database setup
DATABASE = 'hypertension.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with users and predictions tables"""
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                input_data TEXT NOT NULL,
                prediction INTEGER NOT NULL,
                probability REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()

# Load and train model
model = None
scaler = None

def load_model():
    global model, scaler
    try:
        csv_path = r"hypertension_data.csv"
        df = pd.read_csv(csv_path)
        
        # Use all relevant features for better prediction
        # Dataset features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        feature_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        X = df[feature_columns].copy()
        y = df['target']
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        # Train Random Forest Classifier with better parameters
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'  # Handle class imbalance
        )
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        from sklearn.metrics import classification_report, confusion_matrix
        accuracy = (y_pred == y_test).mean()
        
        print(f"\n✓ Random Forest Model trained successfully!")
        print(f"✓ Accuracy: {accuracy:.4f}")
        print(f"✓ Features used: {len(feature_columns)} features")
        print(f"✓ Class distribution - 0: {(y==0).sum()}, 1: {(y==1).sum()}")
        print(f"✓ Model is ready for predictions\n")
        
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============ AUTHENTICATION ROUTES ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username or email already exists'}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=user['id'])
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'username': user['username']
        }), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

# ============ PREDICTION ROUTES ============

@app.route('/api/predict', methods=['POST'])
@jwt_required()
def predict():
    """Make a prediction using the trained Random Forest model"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    try:
        # Extract all 13 features in the correct order
        # Feature order: [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        age = float(data.get('age', 0))
        sex = float(data.get('sex', 0))
        cp = float(data.get('cp', 0))
        systolic = float(data.get('systolic', 0))  # maps to trestbps
        cholesterol = float(data.get('cholesterol', 0))  # maps to chol
        fbs = float(data.get('fbs', 0))
        restecg = float(data.get('restecg', 0))
        heart_rate = float(data.get('heart_rate', 0))  # maps to thalach
        exang = float(data.get('exang', 0))
        oldpeak = float(data.get('oldpeak', 0.3))
        slope = float(data.get('slope', 1))
        ca = float(data.get('ca', 0))
        thal = float(data.get('thal', 3))
        
        # Create feature array in the correct order expected by the model
        features = np.array([[age, sex, cp, systolic, cholesterol, fbs, restecg, heart_rate, exang, oldpeak, slope, ca, thal]])
        
        print(f"\n--- PREDICTION DEBUG ---")
        print(f"Raw features: age={age}, sex={sex}, cp={cp}, systolic={systolic}, chol={cholesterol}")
        print(f"             fbs={fbs}, restecg={restecg}, hr={heart_rate}, exang={exang}, oldpeak={oldpeak}")
        print(f"             slope={slope}, ca={ca}, thal={thal}")
        
        # Scale the input using the trained scaler
        features_scaled = scaler.transform(features)
        print(f"Scaled features (first 5): {features_scaled[0][:5]}")
        
        # Make prediction using Random Forest Classifier
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        prob_class_0 = probabilities[0]
        prob_class_1 = probabilities[1]
        probability = probabilities[prediction]
        
        print(f"Probabilities: Class 0={prob_class_0:.4f}, Class 1={prob_class_1:.4f}")
        print(f"Prediction: {prediction} (Probability: {probability:.4f})")
        print(f"--- END DEBUG ---\n")
        
        # Store prediction in database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO predictions (user_id, input_data, prediction, probability) VALUES (?, ?, ?, ?)',
            (user_id, str(data), int(prediction), float(probability))
        )
        conn.commit()
        conn.close()
        
        # Get health feedback and location if needed
        user_location = data.get('location', None)
        feedback = get_health_feedback(prediction, user_location)
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability),
            'prob_class_0': float(prob_class_0),
            'prob_class_1': float(prob_class_1),
            'feedback': feedback,
            'status': 'success'
        }), 200
    except Exception as e:
        import traceback
        print(f"Prediction error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'message': f'Error making prediction: {str(e)}'}), 400

@app.route('/api/prediction-history', methods=['GET'])
@jwt_required()
def prediction_history():
    """Get user's prediction history"""
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, prediction, probability, created_at FROM predictions WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    )
    predictions = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(p) for p in predictions]), 200

# ============ HEALTH FEEDBACK ============

def get_nearby_doctors(location=None):
    """Get doctors near user's location using location data"""
    # Sample doctors database - in production, integrate with Google Places API
    # For now, returning sample data
    cardiologists = [
        {'name': 'Dr. Rajesh Sharma', 'specialty': 'Cardiology', 'rating': '4.8★', 'distance': '2.3 km', 'phone': '+91-9876543210', 'address': 'Heart Care Clinic, Downtown'},
        {'name': 'Dr. Amit Kumar', 'specialty': 'Cardiology', 'rating': '4.9★', 'distance': '1.8 km', 'phone': '+91-9876543211', 'address': 'Cardiac Center, Main Street'},
        {'name': 'Dr. Priya Patel', 'specialty': 'Internal Medicine', 'rating': '4.7★', 'distance': '3.1 km', 'phone': '+91-9876543212', 'address': 'Health Plus Clinic, Park Avenue'}
    ]
    
    # In production, filter based on actual user location from Google Maps
    if location:
        print(f"Location received: {location}")
        # Use Google Places API to find actual doctors near location
        # For now, return sample data sorted by distance
        return cardiologists
    
    return cardiologists[:2]  # Return only 2 doctors by default

def get_health_feedback(prediction, location=None):
    """Provide personalized health feedback based on prediction"""
    if prediction == 1:  # High BP (Hypertension)
        # Get nearby doctors only for high BP cases
        nearby_doctors = get_nearby_doctors(location)
        
        return {
            'status': 'HIGH BLOOD PRESSURE DETECTED',
            'severity': 'HIGH',
            'tips': [
                '🚫 Reduce salt intake to less than 6g per day',
                '💪 Exercise regularly: 30 minutes, 5 days a week',
                '🍎 Eat more fruits and vegetables',
                '🚭 Quit smoking and limit alcohol',
                '😌 Practice stress management and meditation',
                '⏰ Maintain a healthy sleep schedule (7-9 hours)',
                '⚖️ Maintain a healthy weight'
            ],
            'action': '🏥 IMPORTANT: Contact a healthcare consultant immediately for proper diagnosis and treatment',
            'doctors': nearby_doctors,
            'doctor_note': 'These are recommended cardiologists and internal medicine specialists near you. Please call to confirm availability.'
        }
    else:  # Normal BP (Healthy)
        return {
            'status': 'HEALTHY BLOOD PRESSURE',
            'severity': 'NORMAL',
            'tips': [
                '🏃 Continue regular cardiovascular exercises',
                '🥗 Maintain a balanced diet with whole grains',
                '💧 Stay hydrated with 8-10 glasses of water daily',
                '🧘 Practice yoga or meditation for mental health',
                '🌙 Maintain consistent sleep patterns',
                '🚶 Take a 30-minute walk daily',
                '⏸️ Limit caffeine and processed foods'
            ],
            'action': '✨ Keep up the good health habits! Regular check-ups are recommended.',
            'doctors': [],  # No doctor recommendations for healthy people
            'doctor_note': 'You are in good health. Consider visiting a general physician for annual check-ups.'
        }

# ============ PAGE ROUTES ============

@app.route('/')
def home():
    """Serve the home/login page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page"""
    return render_template('dashboard.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found'}), 404

if __name__ == '__main__':
    init_db()
    if load_model():
        app.run(debug=True, port=5000)
    else:
        print("Failed to load model")
