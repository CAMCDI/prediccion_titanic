import pandas as pd
import joblib
import json
import os
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

# Cargar modelos una vez
try:
    model_path = os.path.join(settings.BASE_DIR, 'models', 'model_titanic.pkl')
    scaler_path = os.path.join(settings.BASE_DIR, 'models', 'scaler.pkl')
    le_sex_path = os.path.join(settings.BASE_DIR, 'models', 'le_sex.pkl')
    le_embarked_path = os.path.join(settings.BASE_DIR, 'models', 'le_embarked.pkl')
    le_title_path = os.path.join(settings.BASE_DIR, 'models', 'le_title.pkl')
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le_sex = joblib.load(le_sex_path)
    le_embarked = joblib.load(le_embarked_path)
    le_title = joblib.load(le_title_path)
    models_loaded = True
except Exception as e:
    print(f"Error cargando modelos: {e}")
    models_loaded = False

def home(request):
    """Servir la página principal"""
    try:
        with open(os.path.join(settings.BASE_DIR, 'templates', 'index.html'), 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    except Exception as e:
        return HttpResponse(f"Error cargando template: {e}")

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def post(self, request):
        if not models_loaded:
            return JsonResponse({"error": "Modelos no cargados correctamente"}, status=500)
        
        try:
            # Parsear JSON
            data = json.loads(request.body)
            
            # Validar campos requeridos
            required_fields = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked', 'Title']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Campo requerido faltante: {field}"}, status=400)
            
            # Asignar Fare basado en Pclass
            fares_by_class = {1: 512, 2: 100, 3: 50}
            fare = fares_by_class[data['Pclass']]
            
            # Calcular FamilySize e IsAlone
            family_size = data['SibSp'] + data['Parch'] + 1
            is_alone = 1 if family_size == 1 else 0
            
            # Crear DataFrame para predicción
            passenger_data = {
                'Pclass': [data['Pclass']],
                'Sex': [data['Sex']],
                'Age': [data['Age']],
                'SibSp': [data['SibSp']],
                'Parch': [data['Parch']],
                'Fare': [fare],
                'Embarked': [data['Embarked']],
                'FamilySize': [family_size],
                'IsAlone': [is_alone],
                'Title': [data['Title']]
            }
            
            df = pd.DataFrame(passenger_data)
            
            # Transformar variables categóricas
            df["Sex"] = le_sex.transform(df["Sex"])
            df["Embarked"] = le_embarked.transform(df["Embarked"])
            df["Title"] = le_title.transform(df["Title"])
            
            # Escalar y predecir
            data_scaled = scaler.transform(df)
            pred = model.predict(data_scaled)[0]
            
            resultado = "🟢 Sobrevive" if pred == 1 else "🔴 No sobrevive"
            
            return JsonResponse({"prediction": resultado})
            
        except ValueError as e:
            return JsonResponse({"error": f"Valor no reconocido: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error en predicción: {str(e)}"}, status=500)