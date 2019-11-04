from locust import HttpLocust, TaskSet, task


class Tasks(TaskSet):
    @task(1)
    def get_reason(self):
        self.client.get("/")

class User(HttpLocust):

    # Set tasks.
    task_set = Tasks

    # Set time in milliseconds between tasks.
    min_wait = 10
    max_wait = 20
