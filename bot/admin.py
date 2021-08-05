from django.contrib import admin

from bot.models import Drug, Category

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('names',)
    search_fields = ['names',]


@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]

