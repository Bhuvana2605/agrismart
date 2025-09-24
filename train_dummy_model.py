import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Dummy data: [temperature, humidity, rainfall]
X = np.array([
    [30, 80, 200],  # Rice
    [22, 60, 50],   # Wheat
    [28, 70, 100],  # Maize
    [25, 65, 120],  # Rice
    [20, 55, 40],   # Wheat
    [27, 75, 90],   # Maize
])
y = ['Rice', 'Wheat', 'Maize', 'Rice', 'Wheat', 'Maize']

model = RandomForestClassifier()
model.fit(X, y)

with open('crop_rf_model.pkl', 'wb') as f:
    pickle.dump(model, f)
