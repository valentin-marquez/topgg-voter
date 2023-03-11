from apscheduler.schedulers.background import BackgroundScheduler

from src.util import logger


class Background(BackgroundScheduler):
    """Background scheduler with default interval of 60 minutes
    """
    def __init__(self):
        super().__init__()
        self.default_interval = 60 # minutes
        self.start()

    def add_job(self, func, trigger, **kwargs):
        if trigger == "interval" and "minutes" not in kwargs:
            kwargs["minutes"] = self.default_interval
        super().add_job(func, trigger, **kwargs)
        logger.info(f"Added job {func.__name__} with trigger {trigger} and kwargs {kwargs}")

    def remove_job(self, job_id):
        super().remove_job(job_id)
        logger.info(f"Removed job {job_id}")

    def remove_all_jobs(self):
        super().remove_all_jobs()
        logger.info("Removed all jobs")
    def shutdown(self, wait=True):
        super().shutdown(wait)
        logger.info("Shut down scheduler")

    def start(self, *args, **kwargs):
        return super().start(*args, **kwargs)

    def new_interval(self, minutes):
        self.default_interval = minutes
        logger.info(f"Set new interval to {minutes} minutes")