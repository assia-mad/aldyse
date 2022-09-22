from apscheduler.schedulers.background import BackgroundScheduler
from .happyhour_update import update_happyhour


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_happyhour, 'interval', seconds=10)
    scheduler.start()