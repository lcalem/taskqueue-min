import json
import time

from bson import ObjectId


JSON_HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}


def test_run_task(api_tq):
    '''
    Will test the dummy adding task
    simply using run_task, which should run the task without queuing it
    '''
    # run_task (should give back the results synchronously)
    json_res, _ = api_tq.POST("/tasks/run", data=json.dumps({"taskpath": "tasks.dummy.dummy_tasks.DummyAdd", "params": {"to_add": [1, 2, 4]}}), headers=JSON_HEADERS)
    assert json_res.get("error") is False
    assert json_res.get("result") is 7


def test_send_task(api_tq):
    '''
    Will test the dummy adding task using send_task,
    which should send the task in a queue for the worker to process it
    '''
    res, _ = api_tq.POST("/tasks/enqueue", data=json.dumps({"taskpath": "tasks.dummy.dummy_tasks.DummyAdd", "params": {"to_add": [1, 2, 4]}, "queue": "test1"}), headers=JSON_HEADERS)
    assert res.get("error") is False
    assert ObjectId.is_valid(res.get("job_id"))

    # check job status via api (which checks in the db)
    max_wait = 10
    cur_wait = 0
    while cur_wait < max_wait:
        json_res, _ = api_tq.GET("/tasks/%s" % res["job_id"])
        print(json_res)
        assert "task" in json_res
        task = json_res["task"]
        assert "status" in task
        if task["status"] not in ["queued", "started"]:
            break

        time.sleep(1)
        cur_wait += 1

    # check when it's finished that we have the results
    assert task["status"] == "success"
    assert task["result"] == 7


def test_required_params(api_tq):
    '''
    a task with required params should fail gracefully when we try to run it without those params
    '''
    pass


def test_job_external_storage(api_tq):
    '''
    will test a job that is supposed to store some data in an external database (not the jobs database)
    -> the result we seek will not be in the results returned by the job but will be stored in the DB
    '''
    pass


def test_job_retry(api_tq):
    pass


def test_job_fail(api_tq):
    pass


def test_job_scheduled(api_tq):
    pass
