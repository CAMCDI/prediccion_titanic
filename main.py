from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, conint
import pandas as pd
import joblib
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="API Predicción Titanic")

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/model_titanic.pkl")
scaler = joblib.load("models/scaler.pkl")
le_sex = joblib.load("models/le_sex.pkl")
le_embarked = joblib.load("models/le_embarked.pkl")
le_title = joblib.load("models/le_title.pkl")


class Passenger(BaseModel):
    Pclass: conint(ge=1, le=3)       
    Sex: str
    Age: conint(ge=1, le=100)        
    SibSp: conint(ge=0, le=8)
    Parch: conint(ge=0, le=6)
    Fare: conint()            # se asigna en la función
    Embarked: str
    FamilySize: conint(ge=1)   
    IsAlone: conint(ge=0, le=1)
    Title: str



@app.get("/")
def home():
    return FileResponse("templates/index.html")


@app.post("/predict")
def predict_survival(passenger: Passenger):
   
    fares_by_class = {1: 512, 2: 100, 3: 50}
    passenger.Fare = fares_by_class[passenger.Pclass]

  
    passenger.FamilySize = passenger.SibSp + passenger.Parch + 1
    passenger.IsAlone = 1 if passenger.FamilySize == 1 else 0

  
    data = pd.DataFrame([passenger.dict()])

  
    try:
        data["Sex"] = le_sex.transform(data["Sex"])
        data["Embarked"] = le_embarked.transform(data["Embarked"])
        data["Title"] = le_title.transform(data["Title"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Valor no reconocido: {e}")

  
    try:
        data_scaled = scaler.transform(data)
        pred = model.predict(data_scaled)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")

    resultado = "🟢 Sobrevive" if pred == 1 else "🔴 No sobrevive"
    return {"prediction": resultado}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
