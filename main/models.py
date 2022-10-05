from django.db import models


class DataUser(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=25)
    address_city = models.CharField(max_length=50)


