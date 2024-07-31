from django.contrib import admin
from materials.models import Course


@admin.register(Course)
class CourserAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner")
