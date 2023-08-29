from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=["post"])
    def rate_meal(self, request, pk=None):
        if "stars" in request.data:
            meal = Meal.objects.get(id=pk)
            username = request.data["username"]
            stars = request.data["stars"]
            user = User.objects.get(username=username)
            try:
                rate = Rate.objects.get(user=user.id, meal=meal.id)
                rate.stars = stars
                rate.save()
                serializer = RateSerializer(rate, many=False)
                json = {"message": "Meal Rate Updated", "result": serializer.data}
                return Response(json, status=status.HTTP_202_ACCEPTED)
            except:
                rate = Rate.objects.create(
                    user=user,
                    meal=meal,
                    stars=stars,
                )
                serializer = RateSerializer(rate, many=False)
                json = {"message": "Meal Rate Created", "result": serializer.data}
                return Response(json, status=status.HTTP_201_CREATED)

        else:
            json = {"message": "no data entered"}
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
