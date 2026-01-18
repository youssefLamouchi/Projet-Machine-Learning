# 🏭 Steel Industry Energy Prediction

Projet de Machine Learning pour prédire la consommation d'énergie de l'industrie sidérurgique en utilisant **Random Forest**.

## 📊 Dataset

- **Source** : UCI Machine Learning Repository - Steel Industry Energy Consumption
- **Volume** : ~35,000 lignes
- **Cible** : `Usage_kWh` (consommation d'énergie)

## 🏗️ Architecture

```
Projet-Machine-Learning/
├── backend/              # API Python Flask
│   ├── app.py           # Serveur Flask + Random Forest
│   ├── requirements.txt # Dépendances Python
│   ├── start.bat        # Script de démarrage Windows
│   └── models/          # Modèles sauvegardés (généré)
├── frontend/            # Application Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── train/    # Composant d'entraînement
│   │   │   │   └── predict/  # Composant de prédiction
│   │   │   └── services/
│   │   │       └── ml.service.ts  # Service API
└── Steel_industry_data.csv  # Dataset
```

## 🚀 Installation et Démarrage

### Backend (Python)

1. Ouvrez un terminal dans le dossier `backend/`
2. Double-cliquez sur `start.bat` OU exécutez :

```cmd
cd backend
py -m pip install -r requirements.txt
py app.py
```

Le serveur démarre sur : `http://localhost:5000`

### Frontend (Angular)

1. Ouvrez un **nouveau terminal** dans le dossier `frontend/`
2. Installez les dépendances :

```cmd
cd frontend
npm install
```

3. Démarrez l'application :

```cmd
npm start
```

L'application s'ouvre sur : `http://localhost:4200`

## 📖 Utilisation

### 1️⃣ Entraîner le modèle

1. Allez sur l'onglet **🎯 Entraîner**
2. Uploadez le fichier `Steel_industry_data.csv`
3. Cliquez sur **"Entraîner le modèle"**
4. Visualisez les métriques (MAE, RMSE, R²)

### 2️⃣ Faire des prédictions

1. Allez sur l'onglet **🔮 Prédire**
2. Uploadez un fichier CSV avec les mêmes colonnes (sans `Usage_kWh`)
3. Cliquez sur **"Prédire"**
4. Téléchargez les résultats en CSV

## 🔬 Modèle

**Random Forest Regressor**
- `n_estimators` : 100 arbres
- `max_depth` : 20
- `min_samples_split` : 5
- Split chronologique : 80% train / 20% test

## 📦 Technologies

**Backend**
- Python 3.14+
- Flask (API REST)
- scikit-learn (Random Forest)
- pandas, numpy

**Frontend**
- Angular 18
- TypeScript
- CSS3

## 📊 Métriques

- **MAE** (Mean Absolute Error) : Erreur moyenne absolue
- **RMSE** (Root Mean Squared Error) : Racine de l'erreur quadratique moyenne
- **R²** (Coefficient de détermination) : Qualité de l'ajustement (0-1)

## 👥 Équipe

Projet collaboratif (7 personnes)

## 📝 Notes

- Le modèle est sauvegardé automatiquement dans `backend/models/`
- Les prédictions peuvent être téléchargées en CSV
- Split chronologique pour éviter le data leakage
