from celery import Celery
from celery.schedules import crontab
from app.core.settings import Settings

celery_app = Celery(
    "crm_tasks",
    broker=Settings.CELERY_BROKER_URL,
    backend=Settings.CELERY_BROKER_URL
)

celery_app.conf.timezone = Settings.CELERY_TIMEZONE

celery_app.autodiscover_tasks(["app.workers"], force=True)

celery_app.conf.beat_schedule = {
    "clear-expired-invites-every-hour": {
        "task": "app.workers.invite_tasks.clear_expired_invites_task",
        "schedule": crontab(minute=0, hour="*/1")
    }
}