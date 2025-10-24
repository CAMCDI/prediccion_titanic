from django.urls import path
from .views import HomeView, PredictSurvivalView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('predict', PredictSurvivalView.as_view(), name='predict_no_slash'),

]
