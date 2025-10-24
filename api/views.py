from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from .serializers import PassengerSerializer
from .utils import model, scaler, le_sex, le_embarked, le_title

class HomeView(TemplateView):
    template_name = "index.html"

class PredictSurvivalView(APIView):
    def post(self, request):
        serializer = PassengerSerializer(data=request.data)
        if serializer.is_valid():
            passenger = serializer.validated_data

            # Cálculos automáticos
            fares_by_class = {1: 512, 2: 73, 3: 0}
            passenger['Fare'] = fares_by_class[passenger['Pclass']]
            passenger['FamilySize'] = passenger['SibSp'] + passenger['Parch'] + 1
            passenger['IsAlone'] = 1 if passenger['FamilySize'] == 1 else 0

            data = pd.DataFrame([passenger])
            try:
                data["Sex"] = le_sex.transform(data["Sex"])
                data["Embarked"] = le_embarked.transform(data["Embarked"])
                data["Title"] = le_title.transform(data["Title"])
            except ValueError as e:
                return Response({"detail": f"Valor no reconocido: {e}"}, status=400)

            try:
                data_scaled = scaler.transform(data)
                pred = model.predict(data_scaled)[0]
            except Exception as e:
                return Response({"detail": f"Error en predicción: {e}"}, status=500)

            resultado = "🟢 Sobrevive" if pred == 1 else "🔴 No sobrevive"
            return Response({"prediction": resultado})
        else:
            return Response(serializer.errors, status=400)
