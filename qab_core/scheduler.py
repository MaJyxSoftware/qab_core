import time
from datetime import datetime
import functools
from concurrent.futures import ThreadPoolExecutor

from croniter import croniter


from qab_core.exception import SchedulerInvalidTaskError

class Scheduler(object):

    def __init__(self, app, max_workers=10) -> None:
        super().__init__()

        self.app = app
        self.__executor = ThreadPoolExecutor(max_workers=1)
        self.workers = ThreadPoolExecutor(max_workers=max_workers)
        self.__is_running = False
        self.tasks = []

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def __process(self) -> None:
        self.app.console.debug("Scheduler started")
        run_countdown = 0
        while self.is_running:
            if run_countdown == 0:
                for task in self.tasks:
                    if task.runnable:
                        self.app.console.debug(f"Run task {task}")
                        self.workers.submit(task.run)

                run_countdown = 60 - datetime.now().second + 1
            else:
                run_countdown -= 1
            time.sleep(1)

        self.app.console.debug("Scheduler stopped")

    def add(self, recurrence, func, *args, **kwargs) -> None:
        task = Task(recurrence, func, *args, **kwargs)
        self.tasks.append(task)
        self.app.console.debug(f"Task {task} scheduled")

    def start(self) -> None:
        self.__is_running = True
        self.__executor.submit(self.__process)

    def stop(self) -> None:
        self.__is_running = False
        self.__executor.shutdown(wait=True)
        

class Task(object):
    def __init__(self, recurrence, func, *args, **kwargs) -> None:
        super().__init__()

        if not croniter.is_valid(recurrence):
            raise SchedulerInvalidTaskError("Invalid recurrence")

        self.recurrence = recurrence

        self.name =  f"{func.__module__}.{func.__name__} [args: {args}, kwargs: {kwargs}]"

        self.func = functools.partial(func, *args, **kwargs)
        self.args = args
        self.kwargs = kwargs

        self.next_run = None
        
        self.__schedule_next_run()

    def __repr__(self) -> str:
        return self.name

    def __schedule_next_run(self) -> None:
        schedule_time = croniter(self.recurrence, datetime.now())
        self.next_run = schedule_time.get_next(datetime)

    @property
    def runnable(self) -> bool:
        return self.next_run <= datetime.now()

    def run(self) -> object:
        ret = self.func()
        self.last_run = datetime.now()
        self.__schedule_next_run()
        return ret