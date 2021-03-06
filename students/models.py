from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.utils.text import slugify




# Create search student manager
class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(last_name__icontains=query) |
                Q(first_name__icontains=query) |
                Q(middle_name__icontains=query) |
                Q(notes__icontains=query) |
                Q(ticket__iexact=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


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
        blank=True,
        null=True,
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

    slug = models.SlugField(
        max_length=256,
        unique=True,
        )

    objects = StudentManager()

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

    slug = models.SlugField(
        max_length=256,
        unique=True,
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

    @property
    def ects(self):
        if self.mark >= 90 and self.mark <= 100:
            return 'A'
        elif self.mark >= 80 and self.mark < 90:
            return 'B'
        elif self.mark >= 65 and self.mark < 80:
            return 'C'
            return 'D'
        elif self.mark >= 50 and self.mark < 55:
            return 'E'
        elif self.mark >= 1 and self.mark < 50:
            return 'F'
        else:
            return 'Оцінка ще не виставлена'

    def passfail(self):
        if self.mark >= 50:
            return True
        else:
            return False


class Issue(models.Model):
    """Issues are send to admin from cotact admin form"""

    from_email = models.EmailField(
        'Email адреса',
        )

    subject = models.CharField(
        'Заголовок листа',
        max_length=128,
        )

    message = models.TextField(
        'Текст повідомлення',
        max_length=2560,
        )

    created_date = models.DateTimeField(
        'Дата створення заявки',
        auto_now_add=True,
        )

    is_replied = models.BooleanField(
        'Відправлено',
        default=False,
        )

    class Meta():
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return 'Заявка № {}'.format(self.id)


class Answer(models.Model):
    """Answers are send as a reply to Issues from admin """

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        )

    subject = models.CharField(
        'Заголовок листа',
        max_length=128,
        )

    message = models.TextField(
        'Текст повідомлення',
        max_length=2560,
        )

    answer_date = models.DateTimeField(
        'Дата відповіді',
        auto_now_add=True,
        )

    issue = models.OneToOneField(
        'Issue',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='answer',
        )

    class Meta():
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'

    def __str__(self):
        return 'Відповідь на заявку № {}'.format(self.issue.id)


class MonthJournal(models.Model):
    """Students Monthly Journal"""

    student = models.ForeignKey('Student', verbose_name='Студент', blank=False, unique_for_month='date')
    # we only need yaer and month, so always set day to
    # first day of the month
    date = models.DateField(verbose_name='Дата', blank=False)
    
    for day in range(1, 32):
        locals()['present_day%d' % day] = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Місячний Журнал'
        verbose_name_plural = 'Місячні Журнали'

    def __str__(self):
        return '{}: {}, {}'.format(self.student.last_name, self.date.month, self.date.year)


# Signals
# -----------------------------------------------------------------------------
@receiver(pre_save, sender=Group)
def pre_save_group_slug(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance:
        group = Group.objects.filter(pk=instance.id).first()
        if not instance.slug or group and instance.title != group.title:
            instance.slug = slugify(instance.title)