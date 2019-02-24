import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Student, Group, Rating


# Students
# -----------------------------------------------------------------------------
@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated student into log file"""
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info('Student added: {} {} (ID: {})'.format(student.first_name,
                    student.last_name, student.id))
    else:
        logger.info('Student updated: {} {} (ID: {})'.format(student.first_name,
                    student.last_name, student.id))

@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """Writes information about deleted student into log file"""
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info('Student deleted: {} {} (ID: {})'.format(student.first_name,
                student.last_name, student.id))

# Groups
# -----------------------------------------------------------------------------
@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated group into log file"""
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    if kwargs['created']:
        logger.info('Group added: {} (ID: {})'.format(group.title, group.id))
    else:
        logger.info('Group updated: {} (ID: {})'.format(group.title, group.id))

@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about deleted group into log file"""
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    logger.info('Group deleted: {} (ID: {})'.format(group.title, group.id))
    
# Ratings
# -----------------------------------------------------------------------------
@receiver(post_save, sender=Rating)
def log_group_updated_added_event(sender, **kwargs):
    """Writes information about newly added or updated rating into log file"""
    logger = logging.getLogger(__name__)

    rating = kwargs['instance']
    if kwargs['created']:
        logger.info('Rating added: {} to {} ({})'.format(rating.mark,
                    rating.student, rating.exam_rating.title))
    else:
        logger.info('Rating updated: {} to {} ({})'.format(rating.mark,
                    rating.student, rating.exam_rating.title))

@receiver(post_delete, sender=Rating)
def log_group_deleted_event(sender, **kwargs):
    """Writes information about deleted rating into log file"""
    logger = logging.getLogger(__name__)

    rating = kwargs['instance']
    logger.info('Rating deleted: {} to {} ({})'.format(rating.mark,
                rating.student, rating.exam_rating.title))