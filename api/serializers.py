from rest_framework import serializers

class PassengerSerializer(serializers.Serializer):
    Pclass = serializers.IntegerField(min_value=1, max_value=3)
    Sex= serializers.CharField()
    Age = serializers.IntegerField(min_value=1, max_value=100)
    SibSp = serializers.IntegerField(min_value=0, max_value=8)
    Parch = serializers.IntegerField(min_value=0, max_value=6)
    Fare = serializers.IntegerField(required=False)
    Embarked = serializers.CharField()
    FamilySize = serializers.IntegerField(required=False)
    IsAlone = serializers.IntegerField(required=False, min_value=0, max_value=1)
    Title = serializers.CharField()