from django.db import models

# Create your models here.
class Student(models.Model):
    """Student model"""
    
    class Meta():
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенти'

    first_name = models.CharField(
        "Ім'я",
        max_length=256,
        blank=False
        )

    last_name = models.CharField(
        "Прізвище",
        max_length=256,
        blank=False
        )

    middle_name = models.CharField(
        "По-батькові",
        max_length=256,
        blank=True,
        default=''
        )

    birthday = models.DateField(
        "Дата народження",
        blank=False,
        null=True
        )

    photo = models.ImageField(
        "Фото",
        blank=True,
        null=True
        )

    ticket = models.CharField(
        "Білет",
        max_length=256,
        blank=False
        )

    notes = models.TextField(
        "Додаткові нотатки",
        blank=True
        )

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)