from .scheduler import job
import schedule
import time


def includeme(config):
    schedule.every(1).minute.do(job)
    schedule
