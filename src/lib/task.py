# from rq.job import Job

from mrq.context import log, get_current_job, get_current_worker
from mrq.exceptions import RetryInterrupt, TimeoutInterrupt, MaxRetriesInterrupt, AbortInterrupt
from mrq.task import Task as MrqTask


class TaskParameterError(Exception):
  pass


class MissingTaskParameterError(TaskParameterError):
  pass


class BaseTask(MrqTask):

    def __init__(self):
        # TODO send metric for init
        pass

    def on_success(self):
        pass

    def on_exception(self, exc, params):
        '''
        return false to interrupt the fail
        '''
        # TODO send exception metric
        return True

    def on_timeout(self, timeout_exc, params):
        '''
        return false to interrupt the timeout
        '''
        return True

    def on_retry(self, retry_exc, params):
        '''
        return false to interrupt the retry
        '''
        # TODO send retry metric
        return True

    def on_maxretries(self, exc, params):
        '''
        no you don't interrupt maxretries
        '''
        pass

    def on_abort(self, exc, params):
        '''
        abort is when the worker has been killed or ctrl+c has been issued
        '''
        pass

    def run_wrapped(self, params):
        '''
        entrypoint
        '''

        for p in (self.required_params or []):
            if p not in params:
                raise MissingTaskParameterError("Required param %s is missing" % p)

        try:

            try:

                ret = self.run(params)
                self.on_success()
                return ret

            except Exception as e:
                if self.on_exception(e, params) is False:
                    return
                raise

            except TimeoutInterrupt as e:
                if self.on_timeout(e, params) is False:
                    return
                raise

        except RetryInterrupt as e:
            if self.on_retry(e, params) is False:
                return
            raise

        except MaxRetriesInterrupt as e:
            self.on_maxretries(e, params)
            raise

        except AbortInterrupt as e:
            self.on_abort(e, params)
            raise

    def run(self, params):
        '''
        dispatch run function
        each task should implement a sub-run function to be called by this one (run_with_params)
        '''

        # populate params / do things with params
        self.params = params

        if hasattr(self, "run_with_params"):
            return self.run_with_params()
