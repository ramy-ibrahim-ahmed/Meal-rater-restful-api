from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, create = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            {
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        response = {"message": "wrong way to create rating"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # http://127.0.0.1:8000/api/meals/1/rate_meal/
    @action(detail=True, methods=["post"])
    def rate_meal(self, request, pk=None):
        if "stars" in request.data:
            meal = Meal.objects.get(id=pk)
            user = request.user
            stars = request.data["stars"]
            # username = request.data["username"]
            # user = User.objects.get(username=username)
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
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {"message": "wrong way to update"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {"message": "wrong way to create"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
