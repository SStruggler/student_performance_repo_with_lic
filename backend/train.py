import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

# 1. Load Data
df = pd.read_csv('Student_Performance.csv')

# 2. Preprocess: Create binary target (e.g., 1 if Performance Index >= 60, else 0)
df['Passed'] = (df['Performance Index'] >= 60).astype(int)

X = df[['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 'Sleep Hours', 'Sample Question Papers Practiced']]
y = df['Passed']

# 3. Convert Categorical variables (e.g., 'Yes'/'No' to numeric)
X = X.copy()
X['Extracurricular Activities'] = X['Extracurricular Activities'].map({'Yes': 1, 'No': 0})

# 4. Split and scale data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 5. Train model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# 6. Save model and scaler
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/trained_model.pkl')
joblib.dump(scaler, 'model/scaler.pkl')

print("Model training complete and saved successfully!")
