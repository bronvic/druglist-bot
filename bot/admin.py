from django.contrib import admin

from bot.models import Drug

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('names', 'description',)
    search_fields = ['names',]

