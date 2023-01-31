from django.db import models


class Categorie(models.Model):
    name_categorie = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name_categorie