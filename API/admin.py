from django.contrib import admin
from .models import *


class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'created']
    list_display_links = ['title']
    list_editable = ['price']
    search_fields = ['title', 'description']
    list_filter = ['price']


class RateAdmin(admin.ModelAdmin):
    list_display = ['meal', 'user', 'stars']
    list_filter = ['meal']


admin.site.register(Meal, MealAdmin)
admin.site.register(Rate, RateAdmin)