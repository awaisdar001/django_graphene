"""Scheduler app config"""
from django.apps import AppConfig


class MeetingSchedulerConfig(AppConfig):
    """Scheduler app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler.meeting_scheduler'
