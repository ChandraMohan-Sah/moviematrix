from django.db import models


class Language(models.Model):
    language = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.language



class ProductionCompany(models.Model):
    production_company = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.production_company 
