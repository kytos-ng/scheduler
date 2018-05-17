"""Main module of amlight/scheduler Kytos Network Application.

Schedule jobs to run at defined times
"""

from kytos.core import KytosNApp, log
from kytos.core.helpers import listen_to
#from napps.amlight.scheduler import settings
from apscheduler.schedulers.blocking import BlockingScheduler


class Main(KytosNApp):
    """Main class of amlight/scheduler NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Replace the '__init__' method for the KytosNApp subclass.

        The setup method is automatically called by the controller when your
        application is loaded.

        So, if you have any setup routine, insert it here.
        """
        self._scheduler = BlockingScheduler()

    def execute(self):
        """This method is executed right after the setup method execution.

        You can also use this method in loop mode if you add to the above setup
        method a line like the following example:

            self.execute_as_loop(30)  # 30-second interval.
        """
        self._scheduler.start()

    def shutdown(self):
        """This method is executed when your napp is unloaded.

        If you have some cleanup procedure, insert it here.
        """
        self._scheduler.shutdown()

    @listen_to('amlight/scheduler.add_job')
    def add_job(self, event):
        """Add a job to this scheduler."""
        try:
            job_id = event.content['id']
        except KeyError:
            log.error('Scheduled job must have an id')
            return

        func = event.content['func']
        kwargs = event.content['kwargs']
        self._scheduler.add_job(func, id=job_id, **kwargs)

    @listen_to('amlight/scheduler.remove_job')
    def remove_job(self, event):
        """Remove a job from this scheduler."""
        try:
            job_id = event.content['id']
        except KeyError:
            log.error('Scheduled job must have an id')
            return

        self._scheduler.remove_job(job_id)
