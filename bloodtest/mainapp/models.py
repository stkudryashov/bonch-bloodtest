from django.db import models


class BloodTest(models.Model):
    personal_number = models.PositiveIntegerField()

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True, null=True)

    birthday = models.DateField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.personal_number}-{self.name}{self.surname}'

    class Meta:
        verbose_name = 'Blood Test'
        verbose_name_plural = 'Blood Tests'
        ordering = ['-datetime']
