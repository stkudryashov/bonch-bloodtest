from django.db import models
import uuid


class BloodTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_number = models.PositiveIntegerField()

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True, null=True)

    birthday = models.DateField()
    datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.personal_number}-{self.name}{self.surname}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-datetime']



class Analysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(BloodTest, null=False, on_delete=models.CASCADE, related_name="BloodTest")
    name = models.CharField(null=False, max_length=64)
    datetime = models.DateField(null=False)

    def __str__(self):
        return f'{self.name} ({self.datetime}) - {self.user}'

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analysis'
        ordering = ['-datetime']


class Indicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, max_length=64)
    value = models.FloatField(null=False)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name="analysis")

    def __str__(self):
        return f'{self.name} - {self.analysis}'
