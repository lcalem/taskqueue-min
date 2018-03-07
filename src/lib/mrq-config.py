TASKS = {
    "tasks.dummy.dummy_tasks.DummyAdding": {

        # In seconds, delay before interrupting the job
        "timeout": 3600,

        # Default queue when none is specified in queue_job()
        "queue": "default",

        # Set the status to "maxretries" after retrying that many times
        "max_retries": 3,

        # Seconds before a job in retry status is requeued again
        "retry_delay": 600,

        # Keep jobs with status in ("success", "cancel", "abort") that many seconds in MongoDB
        "result_ttl": 7 * 24 * 3600,
    }
}
