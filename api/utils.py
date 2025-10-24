import joblib 

model = joblib.load("models/model_titanic.pkl")
scaler = joblib.load("models/scaler.pkl")
le_sex = joblib.load("models/le_sex.pkl")
le_embarked = joblib.load("models/le_embarked.pkl")
le_title = joblib.load("models/le_title.pkl")
