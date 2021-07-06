from django.db import models


class BloodTest(models.Model):
    personal_number = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.personal_number}'

    class Meta:
        verbose_name = 'Blood Test'
        verbose_name_plural = 'Blood Tests'
        ordering = ['-datetime']
