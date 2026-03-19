import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load the dataset
csv_path = "hypertension_data.csv"
df = pd.read_csv(csv_path)

# Splitting features and target
X = df.drop(columns=['target'])
y = df['target']

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Making predictions
y_pred = model.predict(X_test_scaled)

# Create a comparison DataFrame
comparison_df = X_test.copy()
comparison_df['Actual (y_test)'] = y_test
comparison_df['Predicted (y_pred)'] = y_pred
comparison_df['Is Accurate'] = comparison_df['Actual (y_test)'] == comparison_df['Predicted (y_pred)']

print("Overall Accuracy:", comparison_df['Is Accurate'].mean() * 100, "%")
print(f"Total Correct Predictions: {comparison_df['Is Accurate'].sum()} out of {len(y_pred)}")

print("\nSample of predictions (First 10 inputs and outputs):")
pd.set_option('display.max_columns', None)
print(comparison_df.head(10).to_string())

print("\nChecking for mismatches in predictions (if any):")
mismatches = comparison_df[~comparison_df['Is Accurate']]
if len(mismatches) > 0:
    print(mismatches.to_string())
else:
    print("No mismatches found. The model predicted exactly the same output as the actual input for the test dataset!")
