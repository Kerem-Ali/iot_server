from django.contrib import admin
from .models import Light


@admin.register(Light)
class LightAdmin(admin.ModelAdmin):
    list_display = ("name","ip","is_on")
    list_display_links  = ("name","ip","is_on")
    list_filter = ("name","ip","is_on")
    search_fields = ("name",)
    

