from django.contrib import admin
from .models import Categorie


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_categorie')
    list_display_links = ('id', 'name_categorie')


admin.site.register(Categorie, CategorieAdmin)