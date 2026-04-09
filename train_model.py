import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score

# Create model folder
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/laptop.csv")

# Features & target
X = df[["Brand", "Processor", "RAM", "Storage", "ScreenSize"]]
y = df["Price"]

# Encode categorical
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_cat = encoder.fit_transform(X[["Brand", "Processor"]])

# Numeric features
X_num = X[["RAM", "Storage", "ScreenSize"]].values

# Combine
X_final = np.concatenate([X_cat, X_num], axis=1)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_final, y, test_size=0.2, random_state=42
)

# Train model (UPGRADED)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)

print(f"✅ Model Accuracy (R2 Score): {score:.2f}")

# Save
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(encoder, open("model/encoder.pkl", "wb"))

print("✅ Model & Encoder saved!")