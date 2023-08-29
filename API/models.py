from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Meal(models.Model):
    title = models.CharField(verbose_name="Meal Name", max_length=50, null=False)
    description = models.TextField(verbose_name="Meal Description", null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    created = models.DateTimeField(verbose_name="Adding Time", auto_now_add=True)

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"
        ordering = ['id']

    def __str__(self):
        return self.title


class Rate(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=False
    )

    class Meta:
        unique_together = (("user", "meal"),)
        index_together = (("user", "meal"),)
        verbose_name = "Rate"
        verbose_name_plural = "Rates"
        ordering = ['id']
