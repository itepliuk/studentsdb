from django.db import models
from django.core.validators import MaxValueValidator

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
        ordering = ['title']

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

class Exam(models.Model):
    
    class Meta():
        verbose_name = 'Екзамен'
        verbose_name_plural = 'Екзамени'
        ordering = ['exam_date']

    title = models.CharField(
        'Назва',
        max_length=256,
        blank=False,
        )

    teacher = models.CharField(
        'Викладач',
        max_length=256,
        blank=False,
        )


    exam_date = models.DateTimeField(
        "Дата іспиту",
        blank=False,
        null=True
        )

    duration = models.CharField(
        'Тривалість',
        max_length=256,
        blank=True,
        )

    exam_group = models.ForeignKey('Group',
        verbose_name='Група',
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )

    def __str__(self):
        if self.exam_group:
            return '{} {} {}'.format(
                self.title, self.teacher, self.exam_group.title)
        else:
            return '{} {}'.format(self.title, self.teacher)

class Rating(models.Model):
    """docstring for Rating"""

    student = models.ForeignKey('Student',
        verbose_name='Студент',
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )

    exam_rating = models.ForeignKey('Exam',
        verbose_name='Екзамен',
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )

    mark = models.PositiveIntegerField(
        'Оцінка', 
        default=0,
        validators=[MaxValueValidator(100, 'Оцінка не може бути більше 100 балів')]
        )

    notes = models.TextField(
        'Додаткові нотатки',
        blank=True,
        )

    class Meta():
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        
    def __str__(self):
        return '{} {}'.format(self.student, self.mark)

    def ects(self):
        if self.mark >= 90 and self.mark <=100:
            return 'A'
        elif self.mark >= 80 and self.mark <90:
            return 'B'
        elif self.mark >= 65 and self.mark <80:
            return 'C'
        elif self.mark >= 55 and self.mark <65:
            return 'D'
        elif self.mark >= 50 and self.mark <55:
            return 'E'
        elif self.mark >= 1 and self.mark <50:
            return 'F'
        else:
            return 'Оцінка ще не виставлена'

    def passfail(self):
        if self.mark >= 50:
            return True
        else:
            return False