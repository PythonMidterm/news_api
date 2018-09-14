from .scheduler import job
import schedule
import time


def includeme(config):
    """ Brings the scheduler into the app using a decorator that the framework
    is looking for.
    """
    schedule.every(1).minute.do(job)
    schedule
