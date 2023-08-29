from rest_framework import serializers
from .models import *


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ("id", "title", "description", "price", "created", "num", "avg")


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = "__all__"
