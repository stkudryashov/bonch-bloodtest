from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_number = models.PositiveIntegerField(verbose_name='СНИЛС')

    name = models.CharField(max_length=32, verbose_name='имя')
    surname = models.CharField(max_length=32, verbose_name='фамилия')
    patronymic = models.CharField(max_length=32, blank=True, null=True, verbose_name='отчество')
    sex = models.BooleanField(choices=((True, "Мужской"), (False, "Женский")), blank=False, null=False, verbose_name='пол')

    birthday = models.DateField(verbose_name='дата рождения')

    city = models.ForeignKey("City", null=False, on_delete=models.NOT_PROVIDED, related_name="City", verbose_name='город')

    def __str__(self):
        return f'{self.personal_number}-{self.name}{self.surname}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Analysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="BloodTest", verbose_name='пациент')
    name = models.CharField(null=False, max_length=64, verbose_name='название')
    datetime = models.DateField(null=False, verbose_name='дата анализа')
    additional_info = models.TextField(null=False, verbose_name='заключение')

    def __str__(self):
        return f'{self.name} ({self.datetime}) - {self.user}'

    class Meta:
        verbose_name = 'Анализ'
        verbose_name_plural = 'Анализы'
        ordering = ['-datetime']


class Indicator(models.Model):
    TYPES = (
        ('RBC', 'Эритроциты'),
        ('WBC', 'Лейкоциты'),
        ('HGB', 'Гемоглобин'),
        ('HCT', 'Гематокрит'),
        ('PLT', 'Тромбоциты'),
        ('MCV', 'Средний объем эритроцита'),
        ('MCH', 'Среднее содеражние гемоглобина в эритроците'),
        ('MCHC', 'Средняя концентрация гемоглобина в эритроците'),
        ('LYM', 'Лимфоциты'),
        ('EOS', 'Эозинофилы'),
        ('MONO', 'Моноциты'),
        ('BAS', 'Базофилы'),
        ('NEUT', 'Нейтрофилы')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.CharField(max_length=5, choices=TYPES, verbose_name='индикатор')
    value = models.FloatField(null=False, verbose_name='значение')
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name="analysis", null=False, default=None, verbose_name='анализ')

    def __str__(self):
        return f'{self.type} - {self.analysis}'

    class Meta:
        verbose_name = 'Индикатор'
        verbose_name_plural = 'Индикаторы'


class City(models.Model):
    region_number = models.IntegerField(null=False, verbose_name='регион')
    name = models.CharField(null=False, max_length=64, verbose_name='город')
    population = models.IntegerField(null=False, verbose_name='население')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Список городов'


class Normals(models.Model):
    name = models.CharField(max_length=16, db_column='name')
    age = models.PositiveIntegerField(db_column='age')
    min_male = models.FloatField(db_column='min_male')
    max_male = models.FloatField(db_column='max_male')
    min_female = models.FloatField(db_column='min_female')
    max_female = models.FloatField(db_column='max_female')

    class Meta:
        managed = False
        db_table = 'normals'


class Info(models.Model):
    name = models.CharField(max_length=16, db_column='name')
    translate = models.CharField(max_length=32, db_column='translate')
    text = models.TextField(db_column='text')

    class Meta:
        managed = False
        db_table = 'info'
