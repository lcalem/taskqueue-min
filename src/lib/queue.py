import traceback

from mrq.context import log, subpool_map, setup_context
from mrq.job import queue_jobs
from mrq.utils import load_class_by_path

setup_context()


def send_task(path, params, **kwargs):
    return send_tasks(path, [params], **kwargs)[0]


def send_tasks(path,
               params_list,
               queue=None,
               sync=False,
               batch_size=1000,
               subpool_size=None):
    if sync:

        def subpool_inner_func(params):
            try:
                return run_task(path, params)
            except Exception as exc:
                trace = traceback.format_exc()
                log.error("Error in send_tasks subpool: %s \n%s" % (exc, trace))
                raise

        if subpool_size is None:
            return [run_task(path, params) for params in params_list]
        else:
            return subpool_map(int(subpool_size), subpool_inner_func, params_list)

    return queue_jobs(path, params_list, queue=queue, batch_size=batch_size)


def run_task(path, params, **kwargs):
    task_class = load_class_by_path(path)
    return task_class().run_wrapped(params, **kwargs)


# RQ version
# with Connection(Redis(config.get("REDIS_HOST"), config.get("REDIS_PORT"), password=config.get("REDIS_PASSWORD"))):
#     q = Queue(queue_name)
#     job = q.enqueue(to_enqueue, task_params, **enqueue_params)

#     print(job.id)
#     return create_response
