import json
from operator import itemgetter

class Pipeline:

    def __init__(self, giphy):
        self.giphy = giphy

    def init_data(self, pipeline_data):
        self.data = pipeline_data
        self.data['state'] = "working"
        self.data['notifications'] = []
        self.data['image'] = self.giphy.randomize_image("working")

        stageiterator = iter(self.order_data(self.data['stages'],"order"))
        first_stage = next(stageiterator)
        first_stage['state'] = "working"
        taskiterator = iter(self.order_data(first_stage['tasks'],"order"))
        first_task = next(taskiterator)
        first_task['state'] = "working"

        for task in taskiterator:
            task['state'] = "pending"

        for stage in stageiterator:
            stage['state'] = "pending"
            for task in stage['tasks']:
                task['state'] = "pending"

    def read(self):
        with open('pipeline.json', 'r') as file_:
            self.data = json.loads(file_.read())

    def write(self):
        with open('pipeline.json', 'w') as file_:
            file_.write(json.dumps(self.data))

    def order_data(self, data, order_by):
        return sorted(data, key=itemgetter(order_by))

    def create_notification(self, notification_data):
        notification_data['order'] = len(self.data['notifications']) + 1
        self.data['notifications'].append(notification_data)

    def fail(self):
        self.data['state'] = "failed"
        self.data['image'] = self.giphy.randomize_image("fail")
        for stage in self.data['stages']:
            if stage['state'] != "success":
                stage['state'] = "failed"
            for task in stage['tasks']:
                if task['state'] != "success":
                    task['state'] = "failed"

    def progress_percentage(self):
        total_tasks = 0
        total_successfully_tasks = 0
        for stage in self.data['stages']:
            for task in stage['tasks']:
                total_tasks = total_tasks + 1
                if task['state'] == 'success':
                    total_successfully_tasks = total_successfully_tasks + 1
        return float(float(total_successfully_tasks)/float(total_tasks)) * 100

    def progress(self):
        stageiterator = iter(self.order_data(self.data['stages'],"order"))

        for stage in stageiterator:
            if stage['state'] == 'working':
                taskiterator = iter(self.order_data(stage['tasks'],"order"))
                for task in taskiterator:
                    if task['state'] == 'working':
                        task['state'] = "success"
                        break

                next_task = next(taskiterator, None)
                if next_task is not None:
                    next_task['state'] = "working"
                else:
                    stage['state'] = "success"
                    next_stage = next(stageiterator, None)
                    if next_stage is not None:
                        next_stage['state'] = "working"
                        self.order_data(next_stage['tasks'],"order")[0]['state'] = "working"
                    else:
                        self.data['state'] = "success"
                        self.data['image'] = self.giphy.randomize_image("win")
                    break
