#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
csv_path = "hypertension_data.csv"
df = pd.read_csv(csv_path)

# Splitting features and target
X = df.drop(columns=['target'])  # Features
y = df['target']  # Target variable

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Training a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:\n', report)


# In[ ]:





# In[ ]:


# Display personalized feedback based on predictions

def get_health_feedback(prediction):
    """Provide personalized health feedback based on prediction"""
    if prediction == 1:  # High BP (Hypertension)
        return {
            'status': '⚠️ HIGH BLOOD PRESSURE DETECTED',
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
            'doctors': [
                {'name': 'Dr. Rajesh Sharma', 'specialty': 'Cardiology', 'rating': '4.8★', 'distance': '2.3 km'},
                {'name': 'Dr. Priya Patel', 'specialty': 'Internal Medicine', 'rating': '4.7★', 'distance': '3.1 km'},
                {'name': 'Dr. Amit Kumar', 'specialty': 'Cardiology', 'rating': '4.9★', 'distance': '1.8 km'}
            ]
        }
    else:  # Normal BP (Healthy)
        return {
            'status': '✅ HEALTHY BLOOD PRESSURE',
            'tips': [
                '🏃 Continue regular cardiovascular exercises',
                '🥗 Maintain a balanced diet with whole grains',
                '💧 Stay hydrated with 8-10 glasses of water daily',
                '🧘 Practice yoga or meditation for mental health',
                '🌙 Maintain consistent sleep patterns',
                '🚶 Take a 30-minute walk daily',
                '⏸️ Limit caffeine and processed foods'
            ],
            'action': '✨ Keep up the good health habits! Regular check-ups are recommended',
            'doctors': [
                {'name': 'Dr. Neha Singh', 'specialty': 'General Practice', 'rating': '4.6★', 'distance': '2.5 km'},
                {'name': 'Dr. Vikram Desai', 'specialty': 'Preventive Medicine', 'rating': '4.7★', 'distance': '3.0 km'}
            ]
        }

# Display personalized feedback for sample predictions
print("\n" + "="*70)
print("PERSONALIZED HEALTH FEEDBACK FOR PATIENTS")
print("="*70 + "\n")

# Show feedback for first 5 predictions
for i in range(min(5, len(y_pred))):
    feedback = get_health_feedback(y_pred[i])
    print(f"\n{'─'*70}")
    print(f"PATIENT {i+1}: {feedback['status']}")
    print(f"{'─'*70}")
    
    print("\n💡 HEALTH TIPS:")
    for tip in feedback['tips']:
        print(f"   {tip}")
    
    print(f"\n{feedback['action']}")
    
    print("\n🏥 RECOMMENDED DOCTORS NEAR YOU:")
    for doctor in feedback['doctors']:
        print(f"   • {doctor['name']} - {doctor['specialty']}")
        print(f"     Rating: {doctor['rating']} | Distance: {doctor['distance']}\n")

print("\n" + "="*70)
print(f"SUMMARY: Out of {len(y_pred)} patients analyzed:")
print(f"  • High Blood Pressure (Hypertension): {sum(y_pred == 1)} patients")
print(f"  • Normal/Healthy: {sum(y_pred == 0)} patients")
print("="*70)

