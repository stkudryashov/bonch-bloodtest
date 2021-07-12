from django.db import models
import uuid


class BloodTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_number = models.PositiveIntegerField()

    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True, null=True)
    sex = models.BooleanField(choices=((True, "Male"), (False, "Female")), blank=False, null=False)

    birthday = models.DateField()

    city = models.ForeignKey("City", null=False, on_delete=models.NOT_PROVIDED, related_name="City")

    def __str__(self):
        return f'{self.personal_number}-{self.name}{self.surname}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Analysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(BloodTest, null=False, on_delete=models.CASCADE, related_name="BloodTest")
    name = models.CharField(null=False, max_length=64)
    datetime = models.DateField(null=False)
    additional_info = models.TextField(null=False, default="-")

    def __str__(self):
        return f'{self.name} ({self.datetime}) - {self.user}'

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analysis'
        ordering = ['-datetime']


class Indicator(models.Model):
    TYPES = (
        ('RBC', 'Эритроциты'),
        ('WBC', 'Лейкоциты'),
        ('HGB', 'Гемоглобин'),
        ('HCT', 'Гематокрит'),
        ('PLT', 'Тромбоциты'),
        ('MCV', 'Средний объём эритроцита'),
        ('MCH', 'Среднее содеражние гемоглобина в эритроците'),
        ('MCHC', 'Средняя концентрация гемоглобина в эритроците'),
        ('LYM%', 'Лимоциты'),
        ('EOS%', 'Эозинофилы'),
        ('MONO%', 'Моноциты'),
        ('BAS%', 'Базофилы'),
        ('NEUT%', 'Нейтрофилы')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(max_length=5, choices=TYPES)
    value = models.FloatField(null=False)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name="analysis", null=False, default=None)

    def __str__(self):
        return f'{self.type} - {self.analysis}'


class City(models.Model):
    region_number = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=64)
    population = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.name}'
