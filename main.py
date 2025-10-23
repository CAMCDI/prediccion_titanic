from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import joblib
import os

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

app = FastAPI(title="API Predicción Titanic")

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Servir archivos estáticos
# ---------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------
# Cargar modelo y objetos
# ---------------------------
MODEL_PATH = "models/model_titanic.pkl"
SCALER_PATH = "models/scaler.pkl"
LE_SEX_PATH = "models/le_sex.pkl"
LE_EMB_PATH = "models/le_embarked.pkl"
LE_TITLE_PATH = "models/le_title.pkl"

if not all(os.path.exists(p) for p in [MODEL_PATH, SCALER_PATH, LE_SEX_PATH, LE_EMB_PATH, LE_TITLE_PATH]):
    df = pd.read_csv("dataset/train.csv")
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["Title"] = df["Name"].str.extract(r' ([A-Za-z]+)\.', expand=False)

    df["Age"].fillna(df["Age"].median(), inplace=True)
    df["Fare"].fillna(df["Fare"].median(), inplace=True)
    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    cols_to_use = ["Pclass","Sex","Age","SibSp","Parch","Fare",
                   "Embarked","FamilySize","IsAlone","Title"]
    X = df[cols_to_use]
    y = df["Survived"]

    le_sex = LabelEncoder().fit(X["Sex"])
    le_embarked = LabelEncoder().fit(X["Embarked"])
    le_title = LabelEncoder().fit(X["Title"])

    X["Sex"] = le_sex.transform(X["Sex"])
    X["Embarked"] = le_embarked.transform(X["Embarked"])
    X["Title"] = le_title.transform(X["Title"])

    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)

    model = LogisticRegression(max_iter=1000).fit(X_scaled, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le_sex, LE_SEX_PATH)
    joblib.dump(le_embarked, LE_EMB_PATH)
    joblib.dump(le_title, LE_TITLE_PATH)
else:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    le_sex = joblib.load(LE_SEX_PATH)
    le_embarked = joblib.load(LE_EMB_PATH)
    le_title = joblib.load(LE_TITLE_PATH)

# ---------------------------
# Modelo de entrada
# ---------------------------
class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    FamilySize: int
    IsAlone: int
    Title: str

# ---------------------------
# Rutas
# ---------------------------
@app.get("/")
def home():
    return FileResponse("templates/index.html")

@app.post("/predict")
def predict_survival(passenger: Passenger):
    data = pd.DataFrame([passenger.dict()])

    try:
        data["Sex"] = le_sex.transform(data["Sex"])
        data["Embarked"] = le_embarked.transform(data["Embarked"])
        data["Title"] = le_title.transform(data["Title"])
    except ValueError as e:
        return {"error": f"Valor no reconocido: {e}"}

    data_scaled = scaler.transform(data)
    pred = model.predict(data_scaled)[0]
    resultado = "Sobrevive ✅" if pred == 1 else "No sobrevive ❌"
    return {"prediction": resultado}
