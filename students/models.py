from django.db import models

# Create your models here.
class Student(models.Model):
    """Student model"""
    male = 'male'
    female = 'female'
    CHOICES = (
        (male, 'Чоловіча'),
        (female, 'Жіноча')
        )

    class Meta():
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенти'
        ordering = ['last_name']

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

    gender = models.CharField(
        "Стать",
        max_length=25,
        blank=False,
        choices=CHOICES,
        default=male
        )

    student_group = models.ForeignKey('Group',
        verbose_name='Група',
        blank=False,
        null=True,
        on_delete=models.PROTECT
        )
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Group(models.Model):
    """Group Model"""
    class Meta():
        verbose_name = 'Група'
        verbose_name_plural = 'Групи'

    title = models.CharField(
        'Назва',
        max_length=256,
        blank=False,
        )

    leader = models.OneToOneField('Student',
        verbose_name='Староста',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )

    notes = models.TextField(
        'Додаткові нотатки',
        blank=True,
        )

    def __str__(self):
        if self.leader:
            return '{} ({} {})'.format(
                self.title, self.leader.first_name, self.leader.last_name)
        else:
            return '{}'.format(self.title)
