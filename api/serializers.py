from rest_framework import serializers

class PassengerSerializer(serializers.Serializer):
    Pclass = serializers.IntegerField()
    Sex = serializers.CharField()
    Age = serializers.IntegerField()
    SibSp = serializers.IntegerField()
    Parch = serializers.IntegerField()
    Embarked = serializers.CharField()
    Title = serializers.CharField()
    IsAlone = serializers.IntegerField(required=False)
    FamilySize = serializers.IntegerField(required=False)
    Fare = serializers.FloatField(required=False)
