from django.contrib import admin

from bot.models import Medicine, MedicineName


@admin.register(Medicine)
class DrugAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicineName)
class CategorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = [
        "name",
    ]
