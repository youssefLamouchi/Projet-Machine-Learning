from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'models/random_forest_model.pkl'
model = None

def prepare_features(df):
    """Prépare les features à partir du DataFrame"""
    df = df.copy()
    
    # Conversion de la date avec format européen (DD/MM/YYYY)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', dayfirst=True)
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['dayofweek'] = df['date'].dt.dayofweek
        df = df.drop('date', axis=1)
    
    # Encodage One-Hot des variables catégorielles
    categorical_cols = ['WeekStatus', 'Day_of_week', 'Load_Type']
    for col in categorical_cols:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], prefix=col, drop_first=False)
    
    return df

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

@app.route('/api/train', methods=['POST'])
def train_model():
    """Entraîne le modèle Random Forest"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        df = pd.read_csv(file)
        
        # Préparation des données
        df_prepared = prepare_features(df)
        
        # Séparation X et y
        if 'Usage_kWh' not in df_prepared.columns:
            return jsonify({'error': 'Colonne Usage_kWh introuvable'}), 400
        
        X = df_prepared.drop('Usage_kWh', axis=1)
        y = df_prepared['Usage_kWh']
        
        # Split chronologique (80/20)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Entraînement Random Forest
        global model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Prédictions
        y_pred = model.predict(X_test)
        
        # Métriques
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Sauvegarde du modèle
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        
        return jsonify({
            'success': True,
            'metrics': {
                'MAE': round(mae, 2),
                'RMSE': round(rmse, 2),
                'R2': round(r2, 4)
            },
            'train_size': len(X_train),
            'test_size': len(X_test),
            'features': list(X.columns)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Fait des prédictions avec le modèle entraîné"""
    try:
        global model
        
        if model is None:
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
            else:
                return jsonify({'error': 'Modèle non entraîné'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        df = pd.read_csv(file)
        
        # Préparation des features
        df_prepared = prepare_features(df)
        
        # Suppression de Usage_kWh si présent
        if 'Usage_kWh' in df_prepared.columns:
            df_prepared = df_prepared.drop('Usage_kWh', axis=1)
        
        # Prédictions
        predictions = model.predict(df_prepared)
        
        return jsonify({
            'success': True,
            'predictions': predictions.tolist(),
            'count': len(predictions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Chargement du modèle si existant
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✓ Modèle chargé depuis {MODEL_PATH}")
    
    app.run(debug=True, port=5000)
