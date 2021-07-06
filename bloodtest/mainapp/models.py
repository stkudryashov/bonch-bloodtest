from django.db import models


class BloodTest(models.Model):
    personal_number = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
