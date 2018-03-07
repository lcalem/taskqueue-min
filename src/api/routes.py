import json

from bson import ObjectId
from flask import Flask, request
from werkzeug.wrappers import Response

from lib.queue import send_task, run_task
from utils import customjsonclone

from lib.mongo.context import connections


app = Flask(__name__)


def create_response(error=False, message="", status_code=200, extra_response=None):
    response = {
        "error": error,
        "message": message
    }
    if extra_response:
        response.update(extra_response)

    r = Response(json.dumps(customjsonclone(response)), mimetype='application/json')
    r.status_code = status_code

    return r


with app.app_context():

    @app.route('/', methods=["GET"])
    def check():
        '''
        basic check route to be able to check if the api is running
        '''
        return create_response(message="[taskqueue] Hello i'm working")

    @app.route('/tasks/enqueue', methods=["POST"])
    def enqueue_job():
        '''
        will enqueue the specified job
        POST data:
        {
            "taskpath": "tasks.dummy.dummy_tasks.DummyAdding",
            "params": {
                // params for the task
            }
            "queue": xxx

            [optional] sync: bool,  [not implemented]
            [optional] timeout: int   // custom timeout for the task execution
            [optional] result_ttl: int   // custom timeout for the task results
        }
        '''
        content = request.json
        if "taskpath" not in content or "params" not in content:
            return create_response(error=True, message="need taskpath and params for enquing job", status_code=400)

        # TODO test if the job exists
        taskpath = content["taskpath"]
        task_params = content["params"]

        # enqueue params for the job
        enqueue_params = dict()
        for option in ["timeout", "result_ttl", "queue"]:
            if option in content:
                enqueue_params[option] = content[option]

        job_id = send_task(taskpath, task_params, **enqueue_params)
        return create_response(extra_response={"job_id": job_id})

    @app.route('/tasks/run', methods=["POST"])
    def run_job():
        '''
        will run the specified job without using the queue
        POST data:
        {
            "taskpath": "tasks.dummy.test_tasks.DummyAdding",
            "params": {
                // params for the task
            }
        }
        '''
        content = request.json
        if "taskpath" not in content or "params" not in content:
            return create_response(error=True, message="need taskpath and params for enquing job", status_code=400)

        taskpath = content["taskpath"]
        task_params = content["params"]

        task_result = run_task(taskpath, task_params)
        return create_response(extra_response={"result": task_result})

    @app.route('/tasks/<job_id>', methods=["GET"])
    def get_task(job_id):
        '''
        returns {task: None} if the job doesn't exist
        returns {task: {}} otherwise
        '''

        task = connections.mongodb_jobs.mrq_jobs.find_one({"_id": ObjectId(job_id)})
        return create_response(extra_response={"task": task})
